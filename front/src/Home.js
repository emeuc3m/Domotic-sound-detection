import React, { useState, useEffect } from "react";

function isObjectEmpty(obj) {
    return Object.keys(obj).length === 0
}
function Home() {

    const [alerts, setAlerts] = useState({})
    const [showAlert, setShowAlert] = useState(false)

    useEffect(() => {
        function getAlerts() {
            fetch('http://localhost:8000/alerts', {
                headers: {
                    'accept': 'application/json'
                }
            })
            .then(result => result.json())
            .then((result) => {
                if (!isObjectEmpty(result)) {
                    setAlerts(result)
                    setShowAlert(true)
                    console.log("|-- Alert received: ", result)
                    setTimeout(function() {
                        setShowAlert(false);
                      }, 5000);
                }
            })
        }
        getAlerts()
        const interval = setInterval(() => getAlerts(), 500)
        
        return () => {
          clearInterval(interval);
        }
    }, [])


    return (
      <div>
        {showAlert &&
            <div
            style={{
                height: "100vh",
                background: "green",
                color: "white",
                fontSize: "30px",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
                fontFamily: "roboto",
                opacity: showAlert ? 1 : 0
              }}
            >
                Sound recognized: {alerts.type}
            </div>
        }
      </div>
    )
}

export default Home;