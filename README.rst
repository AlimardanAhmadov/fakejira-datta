Calling GraphQL queries via client-side JavaScript is nearly identical to the fetch example above with a couple of small differences. 

First, I obviously do not need to import a library to support fetch. 
Second, and more importantly, I do not have access to environment variables. 

It's worth emphasizing that, if your API requires passing some sort of API key or credentials, you will not want to perform this client side as your credentials will be exposed. 
A better solution would be to call a serverless function that has access to these credentials and then calls the API for you, returning the result. 
If your serverless function is written in JavaScript, the Node code from the prior examples would work. 
However, in the case that the API is wide open, let's look at how this is done (note that my example does have an API key, but please do as I say and not as I do...at least, in demos).

One of the great things about GraphQL is that the response is just plain JSON, so consuming the data is easy. 
The nicer part of this is that the response mirrors the query.
So, let's quickly take the example above and utilize the returned data rather than simply displaying it.

The code below takes the JSON response and then transforms it into HTML (using template literals) to append the items to an HTML list.

(async function () {
    const data = JSON.stringify({
        query: `{
            allShippings {
                product
                customer
                shippingStatus
            }
        }`,
    });

    const response = await fetch(
        'http://127.0.0.1:8000/graphql/',
        {
            method: 'post',
            body: data,
            headers: {
            'Content-Type': 'application/json',
            'Content-Length': data.length,
            Authorization:
                'Apikey DONOTSENDAPIKEYS',
            },
        }
    );

    const shippingData = await response.json();
    const templateFn = (product, customer, shippingStatus) =>  ` <tr role="row" class="odd"><td class="sorting_1">${product}</td><td>${customer}</td><td>${shippingStatus}</td></tr>`;
    const shippinglist = document.querySelector("#flexibleData");
    shippingData.data.allShippings.map((shipping) => {
        shippinglist.insertAdjacentHTML(
        'beforeend',
        templateFn(shipping.product, shipping.customer, shipping.shippingStatus)
      );
    });
})();

The output of running this simple example is an unordered list of characters with the episode they appeared in.

HTML output:
    * John Doe -- Some Product_1 -- Initialized
    * John Doe -- Some Product_2 -- Initialized
    * John Doe -- Some Product_2 -- Initialized


🚀 🚀 🚀 Fakejira Admin is a very modern and a shiny customizable admin extension with user friendly and easy to use interfaces. 
The power of it comes from the libraries it uses on both backend and frontend sides which are django-river, django-rest-framework and Vanilla JS.

Note: Create an admin user for yourself if you would like more access (You can login to the fakejira admin panel using your superuser credentials).
