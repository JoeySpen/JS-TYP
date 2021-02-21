fetch("/settings", {
    method: "GET",
    })
    .then(res => res.json())
        .then(response => {
            console.log("Got response");
            console.log(response);
            
            if(response.error){
            printError(response.error);
            return;
            }
            Object.entries(response).forEach(([key, value]) => {
                var elements = document.getElementsByName(key);
                elements.forEach(element => {

                    // If we found an element turn it on
                    if(element.value === value || value === "on"){
                        element.checked = true;

                        // If its a checkbox we force the parent div off because of the bootstrap toggle library
                        // As sometimes this would not update
                        if(element.type == "checkbox"){
                            element.parentElement.classList.remove("off");
                            
                        }
                    }
                });
            });

/*
response.forEach(row => {
//appendNewDream(row.dream);
console.log("parsing...");

});*/
});