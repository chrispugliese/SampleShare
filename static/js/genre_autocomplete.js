document.addEventListener("DOMContentLoaded", function () {
	const genreInput = document.querySelector("#id_genres");
	const suggestionsBox = document.querySelector("#genre-suggestions");
	const selectedGenresContainer = document.querySelector("#selected-genres");
	const addGenreBtn = document.querySelector("#add-genre-btn");
	let selectedGenres = [];

	// Function to fetch genre suggestions
	function searchGenres(query) {
	fetch(`/search-genres/?q=${encodeURIComponent(query)}`)
		.then(response => response.json())
		.then(data => {
			console.log(data.genres); // Process the returned genres
			displaySuggestions(data.genres); // Call to display suggestions
		})
		.catch(error => console.error('Error fetching genres:', error));
	}

	// Display suggestions in the suggestions box
	function displaySuggestions(genres) {
    suggestionsBox.innerHTML = ""; // Clear previous suggestions
	    if (genres.length > 0) {
	        genres.forEach(genre => {
	            const suggestion = document.createElement("button"); // Changed to button
	            suggestion.classList.add("suggestion-item", "btn", "btn-outline-primary"); // Added Bootstrap button classes
	            suggestion.textContent = genre.name;
	            suggestion.addEventListener("click", () => addGenreTag(genre.name));
	            suggestionsBox.appendChild(suggestion);
	        });
	        suggestionsBox.style.display = "block"; // Show suggestions
	    } else {
	        suggestionsBox.style.display = "none"; // Hide if no genres
	    }
	}

	// Add a genre as a tag
	function addGenreTag(genreName) {
		if (!selectedGenres.includes(genreName)) {
			selectedGenres.push(genreName);
			const genreTag = document.createElement("span");
			genreTag.classList.add("genre-tag");
			genreTag.textContent = genreName;

			// Add remove functionality to the tag
			const removeBtn = document.createElement("button");
			removeBtn.textContent = "x";
			removeBtn.addEventListener("click", () => removeGenreTag(genreName, genreTag));
			genreTag.appendChild(removeBtn);

			selectedGenresContainer.appendChild(genreTag);
		}
		genreInput.value = ""; // Clear input field
		suggestionsBox.style.display = "none"; // Hide suggestions
	}

	// Remove a genre tag
	function removeGenreTag(genreName, tagElement) {
		selectedGenres = selectedGenres.filter(genre => genre !== genreName);
		selectedGenresContainer.removeChild(tagElement);
	}

	// Add a new genre if it doesn't exist
	addGenreBtn.addEventListener("click", function () {
		const newGenre = genreInput.value.trim();
		if (newGenre && !selectedGenres.includes(newGenre)) {
			fetch("/create-genre/", { // Updated URL to match the new endpoint
				method: "POST",
				headers: {
					"Content-Type": "application/x-www-form-urlencoded",
					"X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
				},
				body: new URLSearchParams({ 'genreName': newGenre }), // Sending genre name in form-urlencoded
			})
				.then(response => response.json())
				.then(data => {
					if (data.success) {
						addGenreTag(data.genreName); // Use the genre name returned from the server
					} else {
						alert("Genre already exists or could not be created.");
					}
				})
				.catch(error => console.error("Error adding genre:", error));
		} else {
			alert("Please enter a valid genre name.");
		}
	});

	// Event listener for input to fetch suggestions dynamically
	genreInput.addEventListener("input", async function () {
		const query = genreInput.value.trim();
		if (query.length > 0) {
			searchGenres(query);
		} else {
			suggestionsBox.style.display = "none";
		}
	});
});