// Variable at listed  below

// Below are the html document pertaining variable
var continueButton = document.querySelector(".btn")
var parentContainer = document.querySelector(".parentContainer")
var boxWrap = document.querySelector(".box-wrap")
var removeButton = document.querySelector(".backBtn")
var body = document.querySelector(".body")
var scanlines = document.querySelector(".scanlines")
var hideButton = document.querySelectorAll(".hideButton")
var tables = document.querySelectorAll(".table-wrap")
var gainer_low_stocks = document.getElementById("TOP-GAINER-LOW-MC")
var gainer_high_stocks = document.getElementById("TOP-GAINER-HIGH-MC")
var loser_low_stocks = document.getElementById("TOP-LOSER-LOW-MC")
var loser_high_stocks = document.getElementById("TOP-LOSER-HIGH-MC")
var prefered_stock_space = document.getElementById("prefered_stock_space")
var timeButton = document.querySelector(".newData")


// Bellow here are the variables that concern the python files
var parsed_stock_data = JSON.parse(data)
var parsed_prefered_data = JSON.parse(prefered_data)

var gainers = parsed_stock_data[0]
var losers = parsed_stock_data[1]

var gainers_lowest_MC_Stock = gainers.slice(0, 6);
var gainers_highest_MC_Stock = gainers.slice(-6);
var losers_lowest_MC_Stock = losers.slice(0, 6);
var losers_highest_MC_Stock = losers.slice(-6);

// Add some classes for nesscassity
boxWrap.classList.add("displayNone")
removeButton.classList.add("displayNone")

// this function is meant to remove repeating code for the event listeners byonly listing togglers once 
function toggle_event_listners(element) {
    element.addEventListener('click', () => {
        parentContainer.classList.toggle("displayNone")
        boxWrap.classList.toggle("displayNone")
        removeButton.classList.toggle("displayNone")
        body.classList.toggle("bodyBackground")
        scanlines.classList.toggle("displayNone")
    })
}

// Adds a click listner for the continue button
toggle_event_listners(continueButton)

// Adds a click listner for the back button
toggle_event_listners(removeButton)

// Adds a click listner for the hideButton for table and h1 element
hideButton.forEach(function (button, index) {
    button.addEventListener('click', function () {
        var textContent = button.innerHTML;
        if (textContent === 'HIDE') {
            button.innerHTML = 'DISPLAY';
        } else {
            button.innerHTML = 'HIDE';
        }

        tables[index].classList.toggle("displayNone")

    });
});

async function sendPostRequestForNews(data, parentNode) {
    const url = 'http://127.0.0.1:5000/'; // Replace with the actual URL of your Flask app endpoint

    let response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => {
            data.forEach(article => {
                let paragraph = document.createElement("p");
                let br = document.createElement('br')
                paragraph.textContent = article;
                parentNode.appendChild(paragraph);
                parentNode.appendChild(br);
                paragraph.classList.add("cursorPointer")

                paragraph.addEventListener('click', () => {
                    window.open('https://www.google.com/search?q=' + paragraph.textContent, '_blank');
                })
            });
        })
        .catch(error => {
            // Handle any errors that occurred during the fetch
            return error
        });

    return response
}

// Below we will now take the parsed Data and iterate it into elements
function parsedDataToDocumentForNormalStocks(stock_array, appendingBody, href = 4, tickerSymbolname = 1, Stockexchange = 3, name = 0, oneD = 2, markeyCap = 5, price = 6) {
    for (let i = 0; i < stock_array.length; i++) {
        var newRow = document.createElement('tr');

        var newButton = document.createElement('button')
        newButton.textContent = "DELETE"
        newButton.classList.add('delete_button')
        newButton.addEventListener("click", function () {
            this.parentElement.parentElement.removeChild(this.parentElement)
        });

        // Create the table data cells (<td>) and set their content

        var tickerSymbol = document.createElement('td');
        var tickerSymbolLink = document.createElement('a');
        var query = stock_array[i][Stockexchange].toLowerCase() + '-' + stock_array[i][tickerSymbolname].toLowerCase();

        tickerSymbolLink.href = 'https://www.webull.com/quote/' + query;       
        tickerSymbolLink.target = '_blank'; 

        tickerSymbolLink.classList.add("linkStyling")

        tickerSymbolLink.textContent = stock_array[i][tickerSymbolname] + ' / ' + stock_array[i][Stockexchange];
        tickerSymbol.appendChild(tickerSymbolLink)

        var companyName = document.createElement('td');
        companyName.textContent = stock_array[i][name];

        var oneDchange = document.createElement('td');
        var change = stock_array[i][oneD]
        if (change.includes("-")) {
            oneDchange.innerHTML = '<span class="change lossColor">'+ stock_array[i][oneD] +'</span>' + ' / ' + stock_array[i][markeyCap] + "  / $" + stock_array[i][price];
        } else {
            oneDchange.innerHTML = '<span class="change gainColor">'+ stock_array[i][oneD] +'</span>' + ' / ' + stock_array[i][markeyCap] + "  / $" + stock_array[i][price];
        }

        var news = document.createElement('td');

        var requestNews = document.createElement('button')
        requestNews.textContent = "REQUEST NEWS"
        requestNews.classList.add("request_button")
        requestNews.addEventListener("click", function () {
            this.textContent = "LOADING..."
            const string_data = stock_array[i][Stockexchange] + '-' + stock_array[i][tickerSymbolname]
            const filtered_data = string_data.toLowerCase()

            sendPostRequestForNews(filtered_data, this.parentNode);
            this.parentNode.removeChild(this);
        });

        news.appendChild(requestNews)


        // Append the table data cells to the new row
        newRow.appendChild(tickerSymbol);
        newRow.appendChild(companyName);
        newRow.appendChild(oneDchange);
        newRow.appendChild(news);
        newRow.appendChild(newButton);

        // Append the new row to the table
        appendingBody.appendChild(newRow);
    }
}

parsedDataToDocumentForNormalStocks(gainers_lowest_MC_Stock, gainer_low_stocks)
parsedDataToDocumentForNormalStocks(gainers_highest_MC_Stock, gainer_high_stocks)
parsedDataToDocumentForNormalStocks(losers_lowest_MC_Stock, loser_low_stocks)
parsedDataToDocumentForNormalStocks(losers_highest_MC_Stock, loser_high_stocks)
parsedDataToDocumentForNormalStocks(parsed_prefered_data, prefered_stock_space, 4, 0, 2, 1, 4, 5, 3)

setInterval(()=>{alert("CLOSE THE TAB AND BREAK THE CODE AND RE-RUN FOR NEW DATA")}, 600000)