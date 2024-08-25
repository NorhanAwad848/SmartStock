from django.shortcuts import render,redirect,get_object_or_404
from .models import Item ,Cart, CartItem,Sale
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from collections import defaultdict
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph,Spacer,Image
from datetime import datetime
# Create your views here.

def create(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        quantity=request.POST.get('quantity')
        price=request.POST.get('price')
        supplier_name=request.POST.get('supplier_name')
        description=request.POST.get('description')
        date=request.POST.get('date')
        image = request.FILES.get('image')
        data = Item(name=name, quantity=quantity, price=price,supplier_name=supplier_name, description=description,date=date,image=image )
        data.save()
        return redirect('items')
            
    return render(request,'pages/create.html')


def items(request):
    return render(request,'pages/items.html',{'item':Item.objects.all()})

def add_to_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    cart = get_or_create_cart(request)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        item=item,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('items')


def get_or_create_cart(request):
    cart_id = request.session.get('cart_id')
    if cart_id:
        cart = get_object_or_404(Cart, id=cart_id)
    else:
        cart = Cart.objects.create()
        request.session['cart_id'] = cart.id
    return cart

def remove_from_cart(request, item_id):
    cart = get_or_create_cart(request)
    cart_item = CartItem.objects.filter(cart=cart, item_id=item_id).first()
    if cart_item:
        cart_item.delete()
    return redirect('cart')

def cart(request):
    cart = get_or_create_cart(request)
    cart_items = cart.items.all()
    subtotal = sum(float(item.item.price )* item.quantity for item in cart_items)
    tax = subtotal * 0.05
    shipping = 5.0
    total = subtotal + tax + shipping

    context = {
        'cart': cart_items,
        'subtotal': subtotal,
        'tax': tax,
        'shipping': shipping,
        'total': total,
    }
    return render(request, 'pages/cart.html', context)

def increase_quantity(request, item_id):
    cart = get_or_create_cart(request)
    cart_item = CartItem.objects.filter(cart=cart, item_id=item_id).first()
    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

def decrease_quantity(request, item_id):
    cart = get_or_create_cart(request)
    cart_item = CartItem.objects.filter(cart=cart, item_id=item_id).first()
    if cart_item:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    return redirect('cart')


def checkout(request):
    cart_id = request.session.get('cart_id')
    cart_items = CartItem.objects.filter(cart_id=cart_id)
    for cart_item in cart_items:
        item = cart_item.item
        quantity = cart_item.quantity
        total_price = item.price * quantity

        sale = Sale.objects.create(
            item=item,
            quantity=quantity,
            total_price=total_price
        )
 
        item.quantity -= quantity
        item.save()
        
        CartItem.objects.filter(cart_id=cart_id).delete()
        cart_item.delete()
        
    return redirect('items')

def report(request):
    return render(request,'pages/report.html')


def generate_sales_report(request):
    response = HttpResponse(content_type='application/pdf')
    current_date = datetime.now().strftime("%Y%m%d")
    response['Content-Disposition'] = f'attachment; filename="SmartStock_Sales_Report_{current_date}.pdf"'

    doc = SimpleDocTemplate(
        response,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=100,
        bottomMargin=50,
        title="SmartStock Sales Report",
        author="Norhan Awad", 
    )

    styles = getSampleStyleSheet()
    custom_styles = {
        'Title': ParagraphStyle(
            'Title',
            parent=styles['Title'],
            fontSize=24,
            leading=28,
            alignment=1,  
            spaceAfter=20,
        ),
        'Header': ParagraphStyle(
            'Header',
            parent=styles['Normal'],
            fontSize=12,
            leading=14,
            textColor=colors.grey,
        ),
        'TableHeader': ParagraphStyle(
            'TableHeader',
            parent=styles['Normal'],
            fontSize=12,
            leading=14,
            textColor=colors.whitesmoke,
            alignment=1, 
        ),
        'TableCell': ParagraphStyle(
            'TableCell',
            parent=styles['Normal'],
            fontSize=10,
            leading=12,
            alignment=1,  
        ),
        'Footer': ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=10,
            leading=12,
            alignment=2,  
            textColor=colors.grey,
        ),
    }


    elements = []

    logo_path = 'E:\Software House Solutions\SmartStock\SmartStock\static\image\SWH - logo.png'  
    try:
        logo = Image(logo_path, width=1.5*inch, height=1*inch)
        logo.hAlign = 'LEFT'
        elements.append(logo)
    except:
        pass  

    company_info = Paragraph(
        "Software House Solutions .<br/>99 Omar Bn Elkhatib, Almazah,<br/>Cairo, 02, 02<br/>Phone: (123) 456-7890",
        custom_styles['Header']
    )
    elements.append(company_info)
    elements.append(Spacer(1, 20))

    report_title = Paragraph("Sales Report", custom_styles['Title'])
    elements.append(report_title)

    report_metadata = Paragraph(
        f"Date: {datetime.now().strftime('%B %d, %Y')}<br/>Created by: Norhan Awad<br/> Released by : SmartStock",
        styles['Normal']
    )
    elements.append(report_metadata)
    elements.append(Spacer(1, 20))

    aggregated_sales = defaultdict(lambda: {'quantity': 0, 'revenue': 0})

    sales = Sale.objects.all()
    for sale in sales:
        item_name = sale.item.name
        quantity = sale.quantity
        price_per_unit = sale.item.price
        revenue = price_per_unit * quantity

        aggregated_sales[item_name]['quantity'] += quantity
        aggregated_sales[item_name]['revenue'] += revenue

    table_data = [
        [
            Paragraph("Item Name", custom_styles['TableHeader']),
            Paragraph("Quantity Sold", custom_styles['TableHeader']),
            Paragraph("Price Per Unit", custom_styles['TableHeader']),
            Paragraph("Total Revenue", custom_styles['TableHeader']),
        ]
    ]

    total_quantity = 0
    total_revenue = 0
    for item_name, data in aggregated_sales.items():
        table_data.append([
            Paragraph(item_name, custom_styles['TableCell']),
            Paragraph(str(data['quantity']), custom_styles['TableCell']),
            Paragraph(f"${data['quantity'] and data['revenue']/data['quantity']:.2f}", custom_styles['TableCell']),
            Paragraph(f"${data['revenue']:.2f}", custom_styles['TableCell']),
        ])
        total_quantity += data['quantity']
        total_revenue += data['revenue']

    table_data.append([
        Paragraph("<b>Total</b>", custom_styles['TableCell']),
        Paragraph(f"<b>{total_quantity}</b>", custom_styles['TableCell']),
        Paragraph("-", custom_styles['TableCell']),
        Paragraph(f"<b>${total_revenue:.2f}</b>", custom_styles['TableCell']),
    ])

    table = Table(table_data, colWidths=[150, 100, 100, 100])
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0/255, 102/255, 204/255)),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.lightgrey]),
        ('BACKGROUND', (0, -1), (-1, -1), colors.Color(230/255, 230/255, 230/255)),
    ])
    table.setStyle(table_style)
    elements.append(table)
    elements.append(Spacer(1, 20))

    summary = Paragraph(
        f"<b>Summary:</b><br/>Total Items Sold: {total_quantity}<br/>Total Revenue: ${total_revenue:.2f}",
        styles['Normal']
    )
    elements.append(summary)

    def add_page_number(canvas, doc):
        page_num = canvas.getPageNumber()
        text = f"Page {page_num}"
        canvas.setFont('Helvetica', 9)
        canvas.drawRightString(7.5 * inch, 0.5 * inch, text)

    def set_pdf_metadata(canvas, doc):
        canvas.setTitle("SmartStock Sales Report")
        canvas.setAuthor("Norhan Awad")
        canvas.setSubject("Sales report for SmartStock")
        canvas.setCreator("SmartStock Inc.")

    doc.build(elements, onFirstPage=lambda c, d: (add_page_number(c, d), set_pdf_metadata(c, d)), onLaterPages=add_page_number)

    return response
