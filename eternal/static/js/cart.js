console.log("cart.js")
var updateBtns = document.getElementsByClassName('update-cart')

for (var i = 0; i< updateBtns.length; i++){
		updateBtns[i].addEventListener('click', function(){
		var productId= this.dataset.product
		var action = this.dataset.action
		console.log('productd:', productId, 'action:', action)

		console.log('user:', user)
		if(user === 'AnonymousUser'){
			addCookieItem(productId, action)
			} else{
                updateUserOrder(productId, action)
            }
		})
	}

function addCookieItem(productId, action) {
	console.log("User is not authenticated")

	if(action === 'add'){
		if (cart[productId] === undefined){
			cart[productId] = {'quantity':1}
		}
		else{
			cart[productId]['quantity'] += 1
		}
	}
	if (action === 'remove'){
		cart[productId]['quantity']-=1

		if(cart[productId]['quantity'] <=0){
			console.log('Remove Item')
			delete cart[productId]
		}
	}
	console.log('cart:', cart)
	document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
	location.reload()
}

function updateUserOrder(productId, action){
	console.log('user logged in, sending data...')

	var url = '/update_item/'

	fetch(url, {
	    method: 'POST',
	    headers:{
	        'Content-Type': 'appliction/json',
	        'X-CSRFToken': csrftoken,      //add csrf token from documentation
	    },
	    body: JSON.stringify({'productId': productId, 'action': action})
	})
	.then((response) => {
	    return response.json()
	})
	.then((data) => {
        console.log('data:', data)
        location.reload()
	})
}























//in main.html
//<script type="text/javascript">
//	var user = '{{request.user}}'
//	</script
//
//in views.py
//from django.http import JsonResponse
//
//def updateItem(request):
//	return JsonResponse('Item was added', safe=False)
//
//in urls.py
//path('update_item/', views.updateItem, name="update_item"),

