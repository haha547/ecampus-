const FAQ = document.getElementById("FAQ-alert");
const FAQlg = document.getElementById("FAQ-alert-lg");

function showFAQ() {
    if (window.screen.width>=992){
        if (FAQlg.style.display == "none") {
            FAQlg.style.display = "block";
        } else {
            FAQlg.style.display = "none";
        } 
    } else {
        if (FAQ.style.display == "none") {
            FAQ.style.display = "block";
        } else {
            FAQ.style.display = "none";
        }
    }
    
}

function closeAlert() {
    FAQ.style.display = "none";
}

const course_list = document.getElementById('course-content');

function showContent(){
    if (course_list.style.display == "none") {
        course_list.style.display = "block";
    } else {
        course_list.style.display = "none";
    } 
}
