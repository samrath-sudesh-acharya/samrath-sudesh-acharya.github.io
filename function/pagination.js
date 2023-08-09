// Function to handle pagination
function handlePagination(pageNumber) {
    // Fetch the blog data from the processed_blogs.json file
    fetch('./blog/processed_blogs.json')
      .then(response => response.json())
      .then(blogData => {
        // Number of blogs to display per page
        var blogsPerPage = 12;

        // Generate the HTML content for the given page number
        var htmlContent = generate_blog_html(blogData, pageNumber, blogsPerPage);

        // Update the HTML file by inserting the new blogs into the blog container
        var blogContainer = document.getElementById("blog-container");
        blogContainer.innerHTML = htmlContent;

        // Generate the pagination links and update the pagination section
        var totalBlogs = blogData.length;
        var totalPages = Math.ceil(totalBlogs / blogsPerPage);
        var paginationHTML = '<h3>';
        if (pageNumber > 1) {
          paginationHTML += `<a class="pagination-prev" href="javascript:handlePagination(${pageNumber - 1})">&lt; Previous page</a>`;
        }
        if (pageNumber < totalPages) {
          paginationHTML += `<a class="pagination-next" href="javascript:handlePagination(${pageNumber + 1})">Next page &gt;</a>`;
        }
        paginationHTML += '</h3>';

        var paginationSection = document.getElementById("pagination-section");
        paginationSection.innerHTML = paginationHTML;
      })
      .catch(error => {
        console.error('Error fetching blog data:', error);
      });
  }

  // Call the function to display the initial page (e.g., page 1)
  handlePagination(1);
