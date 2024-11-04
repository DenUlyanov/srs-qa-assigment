# API TEST CASES

Please note: normally test cases would be stored in separate test management tool

## Test Case 1: Add multiple products to cart

Verify that users can add multiple products to their cart and that the cart contains the correct items and quantities.

### Steps:

- Search for products using the search functionality on the website.
- Add each product to the shopping cart.
- Open the cart page to verify its contents.

### Expected Results:

- The cart page should be visible when opened.
- The total number of items in the cart should match the number of products added.
- Each of the products listed above should be present in the cart.

## Test Case 2: Checkout product

Verify that users can search for a product, add it to the shopping cart, and proceed to checkout. The test does not
include payment processing to avoid affecting backend statistics.

### Steps:

- Search for the product using the search functionality on the website.
- Add the product to the shopping cart.
- Open the cart page to verify its contents.
- Verify that the product is present in the cart.
- Proceed to the checkout page.
- Fill in the checkout form without submitting payment.

### Expected Results:

- The cart page should be visible when opened.
- The product should be present in the cart.
- The checkout page should be accessible, and users should be able to fill out the required information in the form.

## Test Case 3: User login

Verify that users can access the login page, enter their credentials, and successfully log in to the website, resulting
in being redirected to the home page.

### Steps:

- Open the login page on the website
- Allow all cookies to ensure proper website functionality.
- Open the cart page to verify its contents.
- Verify that the login page is visible.
- Enter valid email and password credentials.
- Submit the login form.
- Verify that the home page is visible after login.

### Expected Results:

- The login page should be accessible and visible.
- After entering valid credentials, users should be redirected to the home page.

## Test Case 4: Search for valid products

Verify that users can search for products and that the correct number of search results is displayed based on the search
term.

### Steps:

- Search for the product using the search functionality on the website.
- Verify that the search result page is visible.
- Verify that the search results are relevant to the search term.
- Verify that the number of products found matches the expected amount.

### Expected Results:

- The search result page should be visible after submitting the search term.
- The search results should be relevant to the product searched for.
- The number of products found should match the expected result.

## Test Case 5: Search for non-existing products

Verify that searching for a non-existent product returns no results.

### Steps:

- Search for a non-existent product using the search functionality on the website.
- Verify that the search result page is visible.
- Verify that no products are found.

### Expected Results:

- The search result page should be visible after submitting the search term.
- No products should be found for the non-existent product search.
