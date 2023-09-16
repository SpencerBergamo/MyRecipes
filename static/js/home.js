document.addEventListener("DOMContentLoaded", function () {

    const API_KEY = "";
    const BASE_URL = "https://api.spoonacular.com/";

    const daily_tag = document.getElementById("daily_tag");
    const weekly_tag = document.getElementById("weekly_tag");
    const daily_page = document.getElementById("daily_page");
    const weekly_page = document.getElementById("weekly_page");
    var day = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"];

    const header_now = new Date();
    const header_day = header_now.getDay();
    const header_month = header_now.toLocaleString("default", { month: "long" });
    const header_year = header_now.getFullYear();
    const fullDate = `${header_month} ${header_day}, ${header_year}`;

    const header = document.getElementById("header");
    header.innerHTML = fullDate;
    
    daily_tag.addEventListener("click", function (e) {
        e.preventDefault();

        console.log(new Date(8.64e15).toString());

        const container = document.getElementById("daily-container");
        container.innerHTML = "";

        if (daily_page.classList.contains("hidden")) {
            daily_page.classList.remove("hidden");
            weekly_page.classList.add("hidden");
        }

        $.get(`${BASE_URL}mealplanner/generate?timeFrame=day&apiKey=${API_KEY}`, function (data) {
            // const meals = data.meals[1];



            for (let j = 0; j < 3; j++) {
                const div_row = document.createElement("div");
                div_row.setAttribute("class", "daily-row");

                const div_col = document.createElement("div");
                div_col.setAttribute("class", "daily-column");

                const card = document.createElement("div");
                card.setAttribute("class", "daily-card");

                const meals = data.meals[j];

                const a = document.createElement("a");
                a.innerHTML = meals.title;
                a.setAttribute("href", meals.sourceUrl);
                a.setAttribute("target", "_blank");

                card.appendChild(a);
                div_col.appendChild(card);
                div_row.appendChild(div_col);
                container.appendChild(div_row);
            }
        });

    })

    weekly_tag.addEventListener("click", function (e) {

        e.preventDefault();

        const container = document.getElementById("weekly-container");
        container.innerHTML = "";

        if (weekly_page.classList.contains("hidden")) {
            weekly_page.classList.remove("hidden");
            daily_page.classList.add("hidden");
        }

        $.get(`${BASE_URL}mealplanner/generate?timeFrame=week&apiKey=${API_KEY}`, function (data) {



            for (let i = 0; i < day.length; i++) {

                const div_row = document.createElement("div");
                div_row.setAttribute("class", "weekly-row");

                const card = document.createElement("div");
                card.setAttribute("class", "weekly-card");

                for (let j = 0; j < 3; j++) {
                    const meals = data.week[day[i]].meals[j];


                    const a = document.createElement("a");
                    a.innerHTML = `${j + 1}. ${meals.title}`;
                    a.setAttribute("href", meals.sourceUrl);
                    a.setAttribute("target", "_blank");

                    card.appendChild(a);


                }
                div_row.appendChild(card);
                container.appendChild(div_row);
            }
        })
    })





})