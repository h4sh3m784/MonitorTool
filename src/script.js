
const app = document.getElementById('root')

var idToken;
var deviceIp;

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
            
            //Get the menu class
            var menu = document.getElementById("menu")

            //Check if the list exist
            if (menu.innerHTML != null)
                menu.innerHTML = ""

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

    var func = document.getElementById('function').value
    var params = document.getElementById('parameters').value

    params = params.split(',')

    try {
        
        var request = new XMLHttpRequest();
        var url = "https://" + deviceIp + ":5000" + "/math"

        request.open("POST", url);
        request.setRequestHeader('Accept', 'application/json; charset=utf-8')
        
        content = {
            "Call" : {
                "function" : func,
                "parameters" : params
            }
        };
    
        request.onload = function () {
            document.getElementById('output').innerHTML = this.response
        }
    
        request.send(JSON.stringify(content));
    
    }catch (e){
        alert(e);
    }
}

function setSelectedDeviceName(selectedDevice) {
    document.getElementById("selected-device-id").textContent = "selected device: " + selectedDevice
}