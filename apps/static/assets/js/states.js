(async function () {
    const data = JSON.stringify({
        query: `{
            states { 
                slug
                label
                description
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

    const stateData = await response.json();
    console.log(stateData)
    const templateFn = (slug, label, description) =>  ` <tr role="row" class="odd"><td class="sorting_1">${slug}</td><td>${label}</td><td>${description}</td></tr>`;
    const stateList = document.querySelector("#flexibleData");
    console.log(stateList)
    console.log(stateData.data.states);
    stateData.data.states.map((state) => {
        console.log(state.slug)
        stateList.insertAdjacentHTML(
        'beforeend',
        templateFn(state.slug, state.label, state.description)
      );
    });
  })();