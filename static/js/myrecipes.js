document.addEventListener("DOMContentLoaded", function () {
    const API_KEY = "899590b4a5ee45ea8826cc0c10fef5f6";
    const BASE_URL = "https://api.spoonacular.com/";
    const searchButton = document.getElementById('searchButton');
    const searchInput = document.getElementById("searchInput");
    const recipeList = document.getElementById("recipes-list");
    const visitButton = document.getElementById("card-button");
    var temparray = [];
    var activeListing;

    searchButton.addEventListener("click", function (event) {
        event.preventDefault();

        // console.log("search button clicked");

        // clear recipeList
        temparray = [];
        recipeList.innerHTML = "";
        // document.getElementById("recipe-page").classList.remove("hidden");
        var value = encodeURIComponent(searchInput.value);

        // fetch api and retrieve data based on input value
        $.get(`${BASE_URL}recipes/complexSearch?apiKey=${API_KEY}&query=${value}`, function (data) {
            data.results.forEach(function (recipe) {
                if (data.results.length === 0) {
                    // $(".body-recipes").innerHTML = "No results found";
                }
                var info = {
                    recipe_id: recipe.id,
                    title: recipe.title,
                    image: recipe.image,
                }
                temparray.push(info);
            })
            tempListing();
        })
        // console.log(value);
        // console.log(temparray);
        searchInput.value = "";

    })

    visitButton.addEventListener("click", function (e) {
        e.preventDefault();
        visitPage();

    })

    // visitButton.addEventListener("click", function (e) {
    //     e.preventDefault(); 
    //     $.get(`${BASE_URL}recipes/${id.recipe_id}/information?apiKey=${API_KEY}&query=summary`, function (data) {
    // });

    // Create temparray Elements for discover.html page
    function tempListing() {
        for (let i = 0; i < temparray.length; i++) {
            let listing = document.createElement("a");
            listing.setAttribute("href", "#");
            listing.setAttribute("class", "list-group-item list-group-item-action");
            listing.setAttribute("id", temparray[i].recipe_id);
            listing.innerHTML = temparray[i].title;

            listing.addEventListener("click", function (e) {
                e.preventDefault();

                const listings = document.querySelectorAll(".list-group-item-action");
                listings.forEach(item => {
                    item.classList.remove("active");
                });

                listing.classList.add("active");
                console.log(temparray[i])
                previewRecipe(temparray[i]);
            })

            recipeList.append(listing);
        }
    }


    function previewRecipe(id) {
        let cardHeader = document.querySelector(".card-header");
        let cardImage = document.querySelector(".card-img");
        let subheader = document.getElementById("sub-header");
        let cardText = document.getElementById("card-text");
        // let name, visit, score;

        let url = `${BASE_URL}recipes/${id.recipe_id}/information?apiKey=${API_KEY}&includeNutrition=false`;

        $.get(url, function (data) {
            let name = data.sourceName;
            let url = data.sourceUrl;
            let time = data.readyInMinutes;
            activeListing = data;
            // console.log(name);

            cardHeader.innerHTML = id.title;
            cardImage.setAttribute("src", id.image.toString());
            subheader.innerHTML = `${name}`;
            cardText.innerHTML = `Ready in ${time} minutes`;
        })

    }

    function visitPage() {
        // console.log(activeListing);

        if (activeListing && activeListing.sourceUrl) {
            window.open(activeListing.sourceUrl);
        }else{
            console.log("missing info")
        }
    }

})
