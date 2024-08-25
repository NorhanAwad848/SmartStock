document.addEventListener('DOMContentLoaded', function () {
    var check = false;

    function changeVal(el) {
        var parent = el.parentElement;
        var qt = parseFloat(parent.querySelector(".qt").textContent);
        var price = parseFloat(parent.querySelector(".price").textContent);
        var eq = Math.round(price * qt * 100) / 100;
        
        parent.querySelector(".full-price").textContent = eq + "€";
        
        changeTotal();
    }

    function changeTotal() {
        var price = 0;
        var fullPrices = document.querySelectorAll(".full-price");

        fullPrices.forEach(function (item) {
            price += parseFloat(item.textContent);
        });

        price = Math.round(price * 100) / 100;
        var tax = Math.round(price * 0.05 * 100) / 100;
        var shipping = parseFloat(document.querySelector(".shipping span").textContent);
        var fullPrice = Math.round((price + tax + shipping) * 100) / 100;

        if (price === 0) {
            fullPrice = 0;
        }

        document.querySelector(".subtotal span").textContent = price;
        document.querySelector(".tax span").textContent = tax;
        document.querySelector(".total span").textContent = fullPrice;
    }

    document.querySelectorAll(".remove").forEach(function (button) {
        button.addEventListener('click', function () {
            var product = this.closest(".product");
            product.classList.add("removed");
            setTimeout(function () {
                product.style.display = 'none';
                product.remove();
                
                if (document.querySelectorAll(".product").length === 0) {
                    if (check) {
                        document.getElementById("cart").innerHTML = "<h1>The shop does not function, yet!</h1><p>If you liked my shopping cart, please take a second and heart this Pen on <a href='https://codepen.io/ziga-miklic/pen/xhpob'>CodePen</a>. Thank you!</p>";
                    } else {
                        document.getElementById("cart").innerHTML = "<h1>No products!</h1>";
                    }
                }
                changeTotal();
            }, 200);
        });
    });

    document.querySelectorAll(".qt-plus").forEach(function (button) {
        button.addEventListener('click', function () {
            var qtElement = this.parentElement.querySelector(".qt");
            qtElement.textContent = parseInt(qtElement.textContent) + 1;
            
            var fullPriceElement = this.parentElement.querySelector(".full-price");
            fullPriceElement.classList.add("added");

            setTimeout(function () {
                fullPriceElement.classList.remove("added");
                changeVal(button);
            }, 150);
        });
    });

    document.querySelectorAll(".qt-minus").forEach(function (button) {
        button.addEventListener('click', function () {
            var qtElement = this.parentElement.querySelector(".qt");

            if (parseInt(qtElement.textContent) > 1) {
                qtElement.textContent = parseInt(qtElement.textContent) - 1;
            }

            var fullPriceElement = this.parentElement.querySelector(".full-price");
            fullPriceElement.classList.add("minused");

            setTimeout(function () {
                fullPriceElement.classList.remove("minused");
                changeVal(button);
            }, 150);
        });
    });
    setTimeout(function () {
        var isOpenElement = document.querySelector(".is-open");
        if (isOpenElement) {
            isOpenElement.classList.remove("is-open");
        }
    }, 1200);

    document.querySelector(".btn").addEventListener('click', function () {
        check = true;
        document.querySelectorAll(".remove").forEach(function (button) {
            button.click();
        });
    });
});
