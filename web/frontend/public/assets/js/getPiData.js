/**
 * @author  Luca Mikeska
 * @Date    20th September, 2023
 * @Brief   Fetches sensor data from Python API on the Raspberry
 *          Fetched Data will be given to HTML for Output
 */


/**
 * Needed Implementations left
 * Filter functions:
 *    Filter by id
 *    Filter by Date
 *    Filter by co2 range
 *    Filter by temp range
 *    Filter by humid range
 *    Filter by pressure range
 *    Filter by dust range
 *    Filter Attention data
 * 
 *    Add value Type to sensor Readings
 * 
 */

let sensordata;
let filteredData;

function displayData( displayObj, index ){
  document.querySelector("#id_Out").innerHTML         = "id: " + displayObj[index].id;
  document.querySelector("#created_at_Out").innerHTML = "Creation Date: " + displayObj[index].created_at;
  document.querySelector("#co2_Out").innerHTML        = "Co2 Value: " + displayObj[index].co2;
  document.querySelector("#temp_Out").innerHTML       = "Temp Value: " + displayObj[index].temperature;
  document.querySelector("#humid_Out").innerHTML      = "Humidity Value: " + displayObj[index].humidity;
  document.querySelector("#press_Out").innerHTML      = "Pressure Value: " + displayObj[index].pressure;
  document.querySelector("#dust_Out").innerHTML       = "Dust Value: " + displayObj[index].dust;
}

function filterValues(){
  console.log("Start of Function")
  console.log(
    document.getElementById("filterID").value
  );

    filteredData = filterData( sensordata, document.getElementById("filterID").value);
    displayData( filteredData, 0);

  console.log("End of Function")
  /*
  document.querySelector("#filterID")
  document.querySelector("#filterDate")
  document.querySelector("#filterCO2")
  */
}

//Ich glaub das funktioniert so nicht, beziehe daten ja ueber url...
function filterData( jsonObj, filterValue ){
  filteredData = jsonObj.filter(obj => {
    //Add Filter input Array and switch through filter options
    return obj.id == filterValue 
  })
}

function sensorAPI(){
  //fetch("http://172.16.111.9:5555/all");
  fetch("../assets/jsonTest/sensordata.json")
      .then((res) => {
        return res.json();
      })
      .then((sensordata) => {
        
        displayData( sensordata, 3)
        
        console.log("done")
      });
}

function initDataPage() {
  sensorAPI();
  //document.querySelector("#startFilterBtn").onclick = filterValues();
  document.querySelector("#startFilterBtn").addEventListener("click", filterValues());
}


//fetches sensorData from API
document.body.addEventListener(initDataPage());