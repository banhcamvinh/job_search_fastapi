let login_btn = document.getElementById("login")
let username_input = document.getElementById("username")
let password_input = document.getElementById("password")
let token = document.getElementById("token")
login_btn.addEventListener("click",function(){
    username = username_input.value;
    password = password_input.value;

    var xhr = new XMLHttpRequest();
    xhr.open('POST', 'http://127.0.0.1:8000/login', true);
    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhr.onload = function () {
        token.innerText= this.responseText
    };
    xhr.send('username=banhcamvinh121@gmail.com&password=123');
})

let filter_company_btn = document.getElementById("filter_company_btn")
let filter_company_rs = document.getElementById("filter_company_rs")
let filter_company_input = document.getElementById("filter_company_input")
let token_input = document.getElementById("token_input")

filter_company_btn.addEventListener("click",function(){
    var xhr_company = new XMLHttpRequest();
    xhr_company.open('GET', 'http://127.0.0.1:8000/companies/'+filter_company_input.value, true);
    xhr_company.setRequestHeader('Authorization', 'Bearer '+token_input.value);
    xhr_company.responseType = 'json';
    xhr_company.onload = function () {
        console.log(this.responseText);
        filter_company_rs.innerText = this.responseText
    };
    xhr_company.send();
})