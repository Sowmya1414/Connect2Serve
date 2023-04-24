/*template_5u54itp*/
//service_08zooao
//Vf4u076Aejfoy8dnC
function contact(event){
    event.preventDefault();
    const loading=document.querySelector('.popup_overlay-loading')
    const success=document.querySelector('.popup_overlay-success')
    loading.classList+=" popup_overlay--visible"
    emailjs
    .sendForm(
        'service_08zooao',
        'template_5u54itp',
        event.target,
        'Vf4u076Aejfoy8dnC'
    ).then(() => {
       
        loading.classList.remove("popup_overlay--visible")
        success.classList+=" popup_overlay--visible"
      
    }).catch(()=>{
        loading.classList.remove("popup_overlay--visible")
        alert(
            "the email service is temporarily unavailable"
        )
    })
    
    

}
let isPopUpOpen=false
function togglePopUp(){
    
    if(isPopUpOpen){
        isPopUpOpen=false;
        return document.body.classList.remove("popup--open")
    }
    isPopUpOpen=true
      document.body.classList+=" popup--open"
}

let isLoginOpen=false
function togglelogin(){
    
    if(isLoginOpen){
        isLoginOpen=false;
        return document.body.classList.remove("login--open")
    }
    isLoginOpen=true
      document.body.classList+=" login--open"
}