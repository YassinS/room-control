/**
 * @author  Luca Mikeska
 * @Date    20th September, 2023
 * @Brief   Fetches sensor data from Python API on the Raspberry
 *          Fetched Data will be given to HTML for Output
 */

var id = "p_id 2343"; //BIGINT?
var created_at = "p_created_at - 2023-05-20"; //Date format (Acc: .x*6 ms)
var co2 = "p_co2"; //
var temperature = "p_temp"; //C`elsius
var humidity = "p_humid"; //in Percent
var pressure = "p_press"; //
var dust = "p_dust"; //
let dataObj;

function getSensorData() {
  console.log("XX");
  dataObj = fetch("http://172.16.111.9:5555/all"); //JSON.parse("http://172.16.111.9:5555/all");
  console.log(dataObj);
}

// _Out marks TextOutput
function setDisplayData() {
  console.log("setX");
  getSensorData();
  //document.querySelector("#id_Out").innerHTML = dataObj.id[0];
  document.querySelector("#created_at_Out").innerHTML = dataObj.created_at[0];
  document.querySelector("#co2_Out").innerHTML = dataObj.co2[0];
  document.querySelector("#temp_Out").innerHTML = dataObj.temperature[0];
  document.querySelector("#humid_Out").innerHTML = dataObj.humidity[0];
  document.querySelector("#press_Out").innerHTML = dataObj.pressure[0];
  document.querySelector("#dust_Out").innerHTML = dataObj.dust[0];
}
//document.body.addEventListener(getSensorData());
document.body.addEventListener(setDisplayData());
//fetches sensorData from API1
setDisplayData();
