(async function () {
    const data = JSON.stringify({
        query: `{
            allShippings {
                id
                product
                customer
                shippingStatus
            }
        }`,
    });

    console.log(data)

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
    const templateFn = (id, product, customer, shippingStatus) =>  ` <tr role="row" class="odd"><input type="hidden" value="${id}"><td class="sorting_1">${product}</td><td>${customer}</td><td>${shippingStatus}</td></tr>`;
    const shippinglist = document.querySelector("#flexibleData");
    shippingData.data.allShippings.map((shipping) => {
        shippinglist.insertAdjacentHTML(
        'beforeend',
        templateFn(shipping.product, shipping.customer, shipping.shippingStatus)
      );
    });
  })();