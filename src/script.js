
const app = document.getElementById('root')

var idToken;

window.onload = urlParser();

function urlParser(){
    var res = document.location.hash.split(/#|&|=/)
    idToken = res[2];
}

function listDevices() {

    var request = new XMLHttpRequest();

    var url = 'https://wbfppogjp2.execute-api.eu-west-1.amazonaws.com/dev/device';
    
    request.open("GET", url, true);
    request.setRequestHeader("Authorization",idToken);
    
    request.onload = function () {

        if (request.status >= 200 && request.status < 400) {

            var data = JSON.parse(this.response);

            //Check if the list exist
            if (document.getElementById("menu") != null)
                app.removeChild(deviceButtonGroup);

            //Get the menu class
            var menu = document.getElementById("menu")

            //Loop through the retrieved data and create button for each connected device.
            data.forEach(device => {
                const button = document.createElement('a')
                button.textContent = device
                button.setAttribute('href', '#')
                button.onclick = onClickDevice(button)
                menu.append(button)
            })
        }
    }
    request.send();
}


function onClickDevice(button) {
    
    deviceIp = button.textContent
    return false;
};

function onExecute(){
    try {

        var request = new XMLHttpRequest();
        var url = deviceIp + "math";

        request.open("POST", url);
        request.setRequestHeader('Accept', 'application/json; charset=utf-8')
    
        content = {
            "hello": "ONLY IN DEATH DUTY ENDS."
        };
    
        request.onload = function () {
            console.log(this.response)
        }
    
        request.send(JSON.stringify(content));
    
    }catch (e){
        alert(e);
    }
}

function setSelectedDeviceName(selectedDevice) {
    document.getElementById("selected-device-id").textContent = "selected device: " + selectedDevice
}