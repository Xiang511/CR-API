async function getData() {
    const url = "https://api.clashroyale.com/v1/locations/57000228/pathoflegend/players";
    const headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + API_KEY
    };

    try {
        const response = await fetch(url, { headers });
        if (!response.ok) {
            throw new Error(`Response status: ${response.status}`);
        }

        const json = await response.json();
        console.log(json);
    } catch (error) {
        console.error(error.message);
    }
}
API_KEY = ""
getData();