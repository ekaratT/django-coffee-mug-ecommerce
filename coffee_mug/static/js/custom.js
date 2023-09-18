document.addEventListener("click", function (e) {
    if (e.target.className === "menu-list" || e.target.className === "menu-list list-active" || e.target.className === "menu-list logout" || e.target.className === "menu-text") {
        hideMenuBtn()
    }
})

function openMenu(x) {
    // x.classList.toggle("change");
    var sideBar = document.getElementById("sidebar");

    if (sideBar.className === "sidebar") {
        sideBar.className += " responsive";
    } else {
        sideBar.className = "sidebar";
    }
}


function hideMenuBtn() {
    var menu = document.getElementById("sidebar");
    menu.classList.remove("responsive")

}

$(document).ready(function () {
    $('.qty-change').click(function () {
        const action = $(this).attr('data-action');
        const quantityInput = $('.qty');
        let quantity = quantityInput.html();
        if (action === 'decrease') {
            if (quantity > 1) {
                quantity--;
            }
        } else if (action === 'increase') {
            quantity++;
        }
        quantityInput.html(quantity);
    });

    // Add to cart.
    $('.add-to-cart').click(function (e) {
        e.preventDefault();
        var product_id = $(this).attr('data-product-id');
        var override = $(this).attr('data-override');
        var qty = $('#qty-' + product_id).html();
        var url = $(this).attr('data-url');
        // Inspec and take this from product.html
        var token = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            method: 'POST',
            url: url,
            data: {
                'product_id': product_id,
                'qty': qty,
                'override': override,
                csrfmiddlewaretoken: token,
            },
            success: function (response) {
                if (response.status == 'Failed') {
                    swal(response.message, '', 'error')
                } else {
                    swal(response.message, '', 'success')
                    $('#cart-counter').html(response.cart_counter['cart_count']);
                    $('.grand-total-price').html('$' + response.cart_total_price);
                    // checkEmptyCart($('#cart-counter').html());
                }
            }
        })
    })


    $('.cart-update').click(function () {
        var override = $(this).attr('data-override');
        var cart_action = $(this).attr('cart-action');
        var product_id = $(this).closest('.product-data').find('.cart-item-id').val();
        var product_qty = $(this).closest('.product-data').find('.cart-item-qty');
        var quantity = product_qty.html();
        var token = $('input[name=csrfmiddlewaretoken]').val();
        var url = $(this).attr('data-url')

        if (cart_action === 'decrease') {
            if (quantity > 1) {
                quantity--;
            }
        } else if (cart_action === 'increase') {
            quantity++;
        }
        product_qty.html(quantity);

        $.ajax({
            method: 'POST',
            url: url,
            data: {
                'override': override,
                'product_id': product_id,
                'product_qty': quantity,
                csrfmiddlewaretoken: token,
            },
            success: function (response) {
                $('#cart-counter').html(response.cart_counter['cart_count']);
                $('#cart-sub-total').html('$' + response.cart_total);
                $('#cart-fee').html('$' + response.cart_fee);
                $('.grand-total-price').html('$' + response.grand_total);
                // checkEmptyCart($('#cart-counter').html());
            }
        })
    })


    // Delete cart item.
    $('.cart-item-delete').click(function () {
        var cart_id = $(this).closest('.product-data').find('#item-id').val();
        var product_id = $(this).closest('.product-data').find('.cart-item-id').val();
        var url = $(this).attr('data-url');
        // Inspec and take this from product.html
        var token = $('input[name=csrfmiddlewaretoken]').val();
        $.ajax({
            method: 'POST',
            url: url,
            data: {
                'product_id': product_id,
                csrfmiddlewaretoken: token,
            },
            success: function (response) {
                if (response.message == 'Failed') {
                    swal(response.message, '', 'error')
                } else {
                    $('#cart-sub-total').html('$' + response.cart_total);
                    $('#cart-fee').html('$' + response.cart_fee);
                    $('.grand-total-price').html('$' + response.grand_total);
                    deleteCartItemOnPage(0, cart_id);
                    // $('#cart__item__' + cart_id).remove();
                    checkEmptyCart(response.cart_counter);
                    // window.location.href = 'accounts/my-cart/'
                }
            }
        })
    })

    // Check out
    $('.btn-checkout').click(function () {
        var url = $('#place-order').attr('data-url');
        var token = $('input[name=csrfmiddlewaretoken]').val();
        // Send ajax request
        $.ajax({
            type: 'POST',
            url: url,
            data: {
                csrfmiddlewaretoken: token,
                form: $('#checiout-form').serialize()
            },
            success: function (response) {
                if (response.status == 'success') {
                    swal(response.message, '', 'success')
                    $('#cart-sub-total').html('$' + response.cart_total);
                    $('#cart-fee').html('$' + response.cart_fee);
                    $('.grand-total-price').html('$' + response.grand_total);
                } else {
                    swal(response.message, '', 'error')
                }
            },
            error: function (response) {
                alert('error')
            }
        })
    })


    // Go to edit profile page
    $('#btn-edit').click(function () {
        var url = $(this).attr('data-url');
        window.location.href = url;
    })

    // Go to single category page
    $('.category-item').click(function () {
        var url = $(this).attr('data-url');
        window.location.href = url;
    })

    // Go to single product page
    $('.cat-pro-detail').click(function () {
        var url = $(this).attr('data-url');
        window.location.href = url;
    })

    // Save profile changes
    $('.btn-save-change').submit(function (e) {
        e.preventDefault();
        $('#edit-profile').submit();
    })

    // Add active class for menu list
    $('.menu-list').click(function () {
        // remove list-active class from other menu item
        $('.menu-list').removeClass('list-active');

        // Add list-active class
        $(this).addClass('list-active');
    })

    // Add customer comment
    $('#add-comment').click(function (e) {
        e.preventDefault();
        var comment = $('#comment').val();
        var email = $('.comment-email').val();
        console.log(email)
        var url = $(this).attr('data-url');
        var redirect_url = $(this).attr('redirect-url');

        var token = $('input[name=csrfmiddlewaretoken]').val();
        $.ajax({
            method: 'POST',
            url: url,
            data: {
                'comment': comment,
                'email': email,
                csrfmiddlewaretoken: token,
            },
            success: function (response) {
                if (response.message == 'Failed') {
                    swal(response.message, '', 'error')
                } else {
                    window.location.href = redirect_url;
                }
            }
        })
    })

    // Adding product review and product comment
    $('.rating a').click(function (e) {
        e.preventDefault();
        var rating = $(this).attr('data-value');

        // Store rating
        $('.add-product-review').data('rating', rating)

        $('.add-product-review').click(function () {
            var comment = $('#product-review').val();
            var url = $(this).attr('data-url');
            var redirect_url = $(this).attr('redirect-url');
            var token = $('input[name=csrfmiddlewaretoken]').val();
            var product_id = $(this).attr('product-id')

            // Get the stored rating data.
            var rating = $(this).data('rating');

            $.ajax({
                method: 'POST',
                url: url,
                data: {
                    'comment': comment,
                    'rating': rating,
                    'product_id': product_id,
                    csrfmiddlewaretoken: token,
                },
                success: function (response) {
                    if (response.status == 'login_required') {
                        window.location = '/accounts/user-login'
                    }
                    else if (response.status == 'Failed') {
                        swal(response.message, '', 'error')
                    } else {
                        window.location.href = redirect_url;
                    }
                }
            })
        })
    })

    // Proceeding stripe payment
    $('#pay-now').click(function (e) {
        url = $(this).attr('data-url');
        var token = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            method: 'POST',
            url: url,
            data: {
                csrfmiddlewaretoken: token,
            },
            success: function (response) {
                console.log(response.status);
            }
        })
    })

    let renderStar = (rating, container) => {
        var stars = '';
        var fullStars = Math.floor(rating);

        for (var i = 0; i < fullStars; i++) {
            stars += '<span class="cus-rating">★</span>';
        }

        var emptyStar = 5 - Math.ceil(rating);
        for (var j = 0; j < emptyStar; j++) {
            stars += '<span class="cus-rating"></span>';
        }
        // Apply stars to .cus-rating-container class.
        container.children('.cus-rating-container').html(stars);
    }

    let deleteCartItemOnPage = (cartItemQty, cart_id) => {
        if (cartItemQty == 0) {
            document.getElementById('cart__item__' + cart_id).remove();
            window.location = '/accounts/my-cart/';
        }
    }


    // Get stars then call function to render to template.
    $('.product-detail').each(function () {
        var rating = $(this).children('#review-rating').val();
        console.log(rating);
        renderStar(rating, $(this));
    })

    // Go back to home page after payment completed
    $('.completed-icon').click(function () {
        var url = $(this).attr('data-url')
        window.location.href = url;
    })
});



let applyCartAmount = (subtotal, tax, grand_total) => {
    if (window.location.pathname == '/account/my-cart') {
        $('.sub-total').html(subtotal);
        $('.tax').html(tax);
        $('grand-total').html(grand_total);
    }
}

function checkEmptyCart(cart_count) {
    var cart = document.getElementById('cart-wrapper');
    var cart_empty = document.getElementById('empty-cart-wrapper');

    cart.style.display = 'none';
    cart_empty.style.display = 'block';
}

