
const app = document.getElementById('root')

var clientId;

window.onload = urlParser();

function urlParser(){
    var res = document.location.hash.split(/#|&|=/)
    if (res[2] != undefined)
        Window.sessionStorage['idToken'] = res[2]
}

function listDevices() {

    var request = new XMLHttpRequest();

    var url = 'https://wbfppogjp2.execute-api.eu-west-1.amazonaws.com/dev/device';
    
    request.open("GET", url, true);
    request.setRequestHeader("Authorization",Window.sessionStorage['idToken']);
    
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
    clientId = button.textContent
    document.getElementById('currentDevice').innerHTML = "current selected device:" + button.textContent
    return false;
};

function onExecute(){

    var func = document.getElementById('function').value
    var params = document.getElementById('parameters').value

    params = params.split(',')

    try {
        var request = new XMLHttpRequest();
        var url = "https://" + "webrpc.d2c-merapar.toon.eu" + "/rpc/" + String(clientId)

        request.open("POST", url);
        request.withCredentials = true
        request.setRequestHeader('Accept', 'application/json; charset=utf-8')

        content = {
            "Call" : {
                "fusessionStoragenction" : func,
                "parameters" : params
            }
        };
    
        request.onload = function () {
            data = JSON.parse(this.response)
            document.getElementById('output').innerHTML = data['RcpCall']
        }
    
        request.send(JSON.stringify(content));
    
    }catch (e){
        alert(e);
    }
}

function setSelectedDeviceName(selectedDevice) {
    document.getElementById("selected-device-id").textContent = "selected device: " + selectedDevice
}