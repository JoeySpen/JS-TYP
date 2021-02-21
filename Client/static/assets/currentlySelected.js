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
                    //console.log("Checking element: " + element);
                    console.log("key:", key, "value:", value, "element.value:" ,element.value, "element.type" , element.type, "value", value)

                    // Found radio button, so check it
                    if(element.type === "radio" && element.value === value){
                        console.log(1);
                        element.checked = true;
                        return; // Equivalent to continue, but we do this in foreach
                    }

                    
                    
                    // If checkbox setting and not radio button...
                    else if (element.type === "checkbox" && value === "on"){
                        console.log(2);
                        element.checked = true;
                    }else if(element.type === "checkbox" && value === "off"){
                        console.log(3);
                        element.checked = false;
                    }else{
                        console.log(4)
                    }
                });
            });

/*
response.forEach(row => {
//appendNewDream(row.dream);
console.log("parsing...");

});*/
});