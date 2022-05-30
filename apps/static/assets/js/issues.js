(async function () {
    const data = JSON.stringify({
        query: `{
            issues { 
                title
                detail 
                issueStatus
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
    const templateFn = (title, detail, issueStatus) =>  ` <tr role="row" class="odd"><td class="sorting_1">${title}</td><td>${detail}</td><td>${issueStatus}</td></tr>`;
    const stateList = document.querySelector("#flexibleData"); 
    console.log(stateData.data.issues);
    stateData.data.issues.map((issue) => {
        console.log(issue.slug)
        stateList.insertAdjacentHTML(
        'beforeend',
        templateFn(issue.title, issue.detail, issue.issueStatus)
      );
    });
  })();