// Select DOM elements
const loader = document.querySelector("#load");
const loader_tv = document.querySelector("#load_tv");
const moviesContainer = document.querySelector("#movies_container");
const tvContainer = document.querySelector("#tv_container");
const trendingContainer = document.querySelector(".trending_container");
let page = 1;

// Define fetch options
const options = {
    method: ["POST"],
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json', 
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzNGE2Mzg3MjYzYmU4YWFkODNhZGU1ZTA5YjVjNGRiZCIsInN1YiI6IjY1MDkwMzViMzk0YTg3MDExYzllNmM1NCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.An03Ut_9kl-VT8pNRJ83oUajfz0N8SeJu1Cq6zV53EM'
    },
}

// Function to load more data from the API
function loadMoreData(url, parent ) {
    
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.json();
        })
        .then(data => {
            // Append the new data to container
            console.log(data);
            data.results.forEach(element => {
                // name = tv / title = movies
                const type = element["name"] ? "tv" : "movie";
                const title = type === "tv" ? element["name"] : element["title"];
                const media = element["media_type"] ?  element["media_type"] : ""; 
                parent.innerHTML += `
                    <div class="movies card">
                        <img src="https://image.tmdb.org/t/p/w500${element.poster_path}" class="margin-left">
                        <span>Title: <span class="title">${title}</span></span>
                        <span>Rating: <span class="rating">${element.vote_average}</span></span> 
                        ${media ? `<span>Media Type: <span class="title">${media}</span></span>` : ""}
                        <div>
                            ${type === "movie" ?
                             `<button class="btn btn-secondary details" id="${element.id}">Details</button>`
                             +
                            `<button class="btn btn-secondary fav_movie" id="${element.id}">Fav</button>` : 
                            `<button class="btn btn-secondary details_series" id="${element.id}">Details</button>`
                            +
                            `<button class="btn btn-secondary fav_tv" id="${element.id}">Fav</button>`

                        }
                        </div>
                    </div>`;
            });
            page++;
        });
}

document.addEventListener("click", function(event) {
    if (event.target && event.target.id === "load") {
        loadMoreData(`/load-more-data?page=${page + 1}`, moviesContainer, "title");
    }

    if (event.target && event.target.id ==="load_tv"){
        loadMoreData(`/load-more-data-tv?page=${page + 1}`, tvContainer, "name");   
    }

    // request for movies
    if (event.target && event.target.classList.contains("details"))
    {
        const movie_id = event.target.id;
        fetch(`/details?target=${movie_id}`)
        .then(response=>response.text())    
        .then(data=> document.body.innerHTML = data)    
    }
    // request for series.
    if (event.target && event.target.classList.contains("details_series"))
    {
        const tv_id = event.target.id;
        fetch(`/details-tv?tv_id=${tv_id}`)
        .then(response=>response.text())
        .then(data=> document.body.innerHTML = data)
    }

    if (event.target && event.target.classList.contains("fav_movie"))
    {
        const movie_id = event.target.id;
        const postData = {
            movieId : movie_id,
            type : "movie"
        }
        fetch(`/saved-movie?movie_id=${movie_id}`, {
            ...options,
            body: JSON.stringify(postData)
        })
        .then(response => response.text())
        .then(data=> document.body.innerHTML = data)
    }

    if (event.target && event.target.classList.contains("fav_tv"))
    {
        const movie_id = event.target.id;
        const postData = {
            movieId : movie_id,
            type : "tv"
        }
        fetch(`/saved-movie?movie_id=${movie_id}`, {
            ...options,
            body: JSON.stringify(postData)
        })
        .then(response => response.text())
        .then(data=> document.body.innerHTML = data)
    }
}); 

const search = document.querySelector("#search_btn");
const searchInput = document.querySelector("#search");
const detailsContainer = document.querySelector(".details_container");


search?.addEventListener("click", function (event) {
    event.preventDefault();
    if (searchInput.value === "") return;
    input = searchInput.value.trim().replace(" ", "%");
    if (loader){
        loader.style.display = "none"
    }

    if (loader_tv){
        loader_tv.style.display = "none"
    }
    
    if (detailsContainer) return;
   
    // Check if the containers exist before clearing their content
    if (tvContainer) {
        
        tvContainer.innerHTML = "";
        loadMoreData( `/search?query=${input}`, tvContainer)
    }

    if (moviesContainer) {
        moviesContainer.innerHTML = "";
        loadMoreData( `/search?query=${input}`, moviesContainer)
    }

    if (trendingContainer) {
        trendingContainer.innerHTML = "";
        loadMoreData( `/search?query=${input}`, trendingContainer)
    }
}); 