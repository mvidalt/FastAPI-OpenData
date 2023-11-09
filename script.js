function ferPeticioAPI() {
    var xhr = new XMLHttpRequest();
    var url = "https://services1.arcgis.com/nCKYwcSONQTkPA4K/arcgis/rest/services/Playas_2015/FeatureServer/0/query?where=Provincia%20%3D%20'ILLES%20BALEARS'&outFields=*&outSR=4326&f=json"; // URL de l'API

    xhr.open('GET', url, true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4) {
            if (xhr.status == 200) {
                var data = JSON.parse(xhr.responseText);

                // Processa les dades segons les teves necessitats
                // Exemple: Mostra els primers elements de les dades
                var resultatsDiv = document.getElementById('resultats');
                resultatsDiv.innerHTML = '<h2>Dades rebudes de l\'API:</h2>';
                resultatsDiv.innerHTML += '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
            } else {
                // Si la sol·licitud no és exitosa, mostra un missatge d'error
                var resultatsDiv = document.getElementById('resultats');
                resultatsDiv.innerHTML = '<h2>Error en la sol·licitud a l\'API. Codi d\'estat: ' + xhr.status + '</h2>';
            }
        }
    };
    xhr.send();
}
