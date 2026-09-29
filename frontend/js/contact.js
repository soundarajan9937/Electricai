function sendMessage(){

let name=document.getElementById("name").value.trim();

let email=document.getElementById("email").value.trim();

let phone=document.getElementById("phone").value.trim();

let subject=document.getElementById("subject").value.trim();

let message=document.getElementById("message").value.trim();

if(name=="" || email=="" || phone=="" || subject=="" || message==""){

alert("Please fill all fields.");

return;

}

alert("✅ Message Sent Successfully!");

document.getElementById("name").value="";
document.getElementById("email").value="";
document.getElementById("phone").value="";
document.getElementById("subject").value="";
document.getElementById("message").value="";

}