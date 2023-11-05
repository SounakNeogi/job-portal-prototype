// You can add JavaScript functionality here

// Sample code to fetch job listings using JavaScript fetch API
fetch('api/job-listings')
    .then(response => response.json())
    .then(data => {
        const jobListings = document.querySelector('.job-listings');
        data.forEach(job => {
            jobListings.innerHTML += `
                <div class="job-card">
                    <h2>${job.title}</h2>
                    <p>${job.description}</p>
                    <p>Location: ${job.location}</p>
                    <p>Company: ${job.company}</p>
                </div>
            `;
        });
    })
    .catch(error => {
        console.error('Error fetching job listings: ', error);
    });
