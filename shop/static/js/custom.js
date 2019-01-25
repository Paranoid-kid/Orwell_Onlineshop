$('.popup-element')
    .popup({
            inline: true,
            hoverable: true,
            position: 'bottom left',
            delay: {
                show: 200,
                hide: 800
            },
            // on: 'click',
            lastResort: 'bottom right',
            onShow: function () {
                resizePopup();
            },
        }
    );


$('.popup-element-top')
    .popup()
;

$('.ui.star.rating')
    .rating()
;

$('.dropdown')
    .dropdown({transition: 'drop', on: 'hover'})
;

$('.ui.left.sidebar').sidebar({
    dimPage: false,
    transition: 'overlay',
    exclusive: false,
    closable: true,
});

$('.ui.left.sidebar')
    .sidebar('attach events', '#left-sidebar-toggle');

$('.index-dimmer.cards .image').dimmer({
    on: 'hover'
});


$(document).ready(function () {
    $("#show-product-list").click(function () {
        $(".doubling.four.column.row").toggle(300);
    });
});

$('.ui.accordion')
    .accordion()
;

$('#drop-down')
    .dropdown()
;

$('.ui.checkbox')
    .checkbox()
;

var resizePopup = function () {
    $('.ui.popup').css('max-height', $(window).height());
};

$(window).resize(function (e) {
    resizePopup();
});

// -----------------------------Cart-----------------------------
loadCart();

function addToCart(btn) {
    if (isCartEmpty()) {
        $('#isEmpty').hide();
        $('#checkOutButton').show();
        $('#cartListTable').show();
    }
    var $tds = $(btn);
    var pid = $tds.parent().siblings('.prod-pid').html();
    var url = `/api/product/${pid}/`;
    var $trs = $("#goods>tr");

    $.get(url, function (response) {
        var name = response.name;
        var price = response.price;
        for (var i = 0; i < $trs.length; i++) {
            var $gtds = $trs.eq(i).children();
            var gName = $gtds.eq(0).html();
            if (name == gName) {
                var num = parseInt($gtds.eq(2).children().eq(1).val());
                $gtds.eq(2).children().eq(1).val(++num);
                $gtds.eq(3).html(price * num);
                saveCart();
                return;
            }
        }
        var li =
            "<tr>" +
            "<td class='itemName'>" + name + "</td>" +
            "<td class='itemPrice'>" + price + "</td>" +
            "<td align='center'>" +
            "<input type='button' value='-' onclick='decrease(this);'/> " +
            "<input type='text' size='3' readonly value='1'/> " +
            "<input type='button' value='+' onclick='increase(this);'/>" +
            "</td>" +
            "<td>" + price + "</td>" +
            "<td align='center'>" +
            "<input type='button' value='x' onclick='del(this);'/>" +
            "<td class='itemPid' hidden='hidden'>" + pid + "</td>" +
            "</td>" +
            "</tr>";
        $("#goods").append($(li));
        saveCart();
    });
    saveCart();
}


function increase(btn) {
    var $td = $(btn).prev();
    var num = parseInt($td.val());
    $td.val(++num);
    var price = parseInt($(btn).parent().prev().html());
    $(btn).parent().next().html(num * price);
    saveCart();
}

function decrease(btn) {
    var num = parseInt($(btn).next().val());
    if (num <= 1) {
        return;
    }
    $(btn).next().val(--num);
    var price = parseInt($(btn).parent().prev().html());
    $(btn).parent().next().html(price * num);
    saveCart();
}

function del(btn) {
    $(btn).parent().parent().remove();
    saveCart();
    isCartEmpty();
}

function totalNumPrice() {
    var $trs = $("#goods>tr");
    var totalPrice = 0;
    var totalQuantity = 0;
    for (var i = 0; i < $trs.length; i++) {
        var quantity = parseInt($trs.eq(i).children().eq(2).children().eq(1).val());
        totalPrice += parseInt($trs.eq(i).children().eq(3).html());
        totalQuantity += quantity;
    }
    $("#totalQuantity").html(totalQuantity);
    $("#totalPrice").html(totalPrice);
    if ($trs.length > 0) {
        $('#shoppingCartNum').text(totalQuantity);
    } else {
        $('#shoppingCartNum').text('');
    }
}

function saveCart() {
    let $trs = $("#goods>tr");
    let totalPrice = 0;
    let totalQuantity = 0;
    let cartJSON = [];
    for (var i = 0; i < $trs.length; i++) {
        let pid = parseInt($trs.eq(i).children().eq(5).html());
        let quantity = parseInt($trs.eq(i).children().eq(2).children().eq(1).val());
        totalPrice += parseInt($trs.eq(i).children().eq(3).html());
        cartJSON.push({'pid': pid, 'quantity': quantity});
        totalQuantity += quantity;
    }
    $("#totalQuantity").html(totalQuantity);
    $("#totalPrice").html(totalPrice);
    if ($trs.length > 0) {
        $('#shoppingCartNum').text(totalQuantity);
    } else {
        $('#shoppingCartNum').text('');
    }
    localStorage.setItem('shoppingCart', JSON.stringify(cartJSON));
}


function isCartEmpty() {
    var cart = JSON.parse(localStorage.getItem('shoppingCart'));
    if ((Array.isArray(cart) && cart.length === 0) || cart == null) {
        $('#isEmpty').show();
        $('#checkOutButton').hide();
        $('#cartListTable').hide();
        return true;
    }
}

function checkOut() {
    var cart = localStorage.getItem('shoppingCart');
    // var cart = JSON.parse(localStorage.getItem('shoppingCart'));
    // console.log(cart);
    $.ajax({
        url: "/order/checkout/",
        type: 'POST',
        data: {
            'cart': cart,
        },
        dataType: 'json',
        success: function (ret) {
            // console.log(ret.order_id)// http code 200
            window.location.href = "/order/checkout/" + ret.digest + "/";
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            switch (XMLHttpRequest.status) {
                case 401:
                    break;
                case 404:
                    break;
                case 500:
                    break;
            }
        }
    });
}

function loadCart() {
    var cart = JSON.parse(localStorage.getItem('shoppingCart'));
    // console.log(cart);
    if (!isCartEmpty()) {
        for (let i = 0; i < cart.length; i++) {
            let pid = cart[i].pid;
            let url = `/api/product/${pid}/`;
            (function (i) {
                $.get(url, function (response) {
                    let name = response.name;
                    let price = response.price;
                    let quantity = cart[i].quantity;
                    let li =
                        "<tr>" +
                        "<td class='itemName'>" + name + "</td>" +
                        "<td class='itemPrice'>" + price + "</td>" +
                        "<td align='center'>" +
                        "<input type='button' value='-' onclick='decrease(this);'/> " +
                        "<input type='text' size='3' readonly value=" + quantity + "> " +
                        "<input type='button' value='+' onclick='increase(this);'/>" +
                        "</td>" +
                        "<td>" + price * quantity + "</td>" +
                        "<td align='center'>" +
                        "<input type='button' value='x' onclick='del(this);'/>" +
                        "<td class='itemPid' hidden='hidden'>" + pid + "</td>" +
                        "</td>" +
                        "</tr>";
                    $("#goods").append($(li));
                    // saveCart();
                });
            })(i)
        }
    }
    totalNumPrice()
}

function clearCart() {
    localStorage.clear()
}

function loadOrderInfo() {
    var cart = JSON.parse(localStorage.getItem('shoppingCart'));
    if (!isCartEmpty()) {
        for (var i = 0; i < cart.length; i++) {
            var pid = cart[i].pid;
            var url = `/api/product/${pid}/`;
            (function (i) {
                $.get(url, function (response) {
                    var name = response.name;
                    var price = response.price;
                    var quantity = cart[i].quantity;
                    var checkoutinfo =
                        "<tr>" +
                        "<td class='itemName'>" + name + "</td>" +
                        "<td class='itemPrice'>" + "<i class='dollar sign icon'></i>" + price + "</td>" +
                        "<td class=''>" + quantity + "</td>" +
                        "<td>" + "<i class='dollar sign icon'></i>" + price * quantity + "</td>" +
                        "</tr>";
                    $("#checkoutinfo").append($(checkoutinfo));
                });
            })(i)
        }
    }
}