console.log(navigator.serviceWorker);

navigator.serviceWorker.getRegistration("/app").then(reg =>{
    reg.pushManager.subscribe({
        userVisibleOnly: true
    }).then(sub =>{
        console.log(sub);
    })
})