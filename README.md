# Youtube-Analytics-API-Use
An application to fetch data from the Youtube Analytics API with the Flask package

## Requirements:-
* Python>3.7
* pip

## Installation Steps:-
1. Clone the repository

2. Open the directory in the Command Line Interface
    ```
    cd Youtube-Analytics-API-Use
    ```

3. Create a virtual environment (replace the placeholder text below with the name you desire)
    ```
    python3 -m venv VIRTUAL-ENVIRONMENT-NAME
    ```
* you can activate the environment in the terminal with
    ```
    source /VIRTUAL-ENVIRONMENT-NAME/bin/activate
    ```

4. Execute the following pip command to set up packages
    ```
    pip install --upgrade google-api-python-client

    pip install --upgrade google-auth google-auth-oauthlib google-auth-httplib2

    pip install --upgrade flask

    pip install --upgrade requests
    ```

5. Create a project in Google Console and enable the Youtube Analytics API

6. From the project dashboard click on OAuth consent screen to set it up (remember to add your gmail account to the list of Test User when in the testing phase)

7. After finishing the setup of th OAuth consent screen go to the Credentials tab, select the "CREATE CREDENTIALS" and then select "OAuth client ID" option

8. Select "Web application" as the Application type, enter the other relevant detauls
    * for local testing remember to add "http://localhost:8080/oauth2callback" as the authorized redirect URI

9. Once the OAuth 2.0 CLient ID is created download the client secret json file

10. Place the json file in the root of the folder rename it to "client_secrets.json"

11. Once all the above steps are done, simply run the python file and open the following url in your web browser
    ```
    http://localhost:8080
    ```