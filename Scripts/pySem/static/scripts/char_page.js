let chart;

const r_input = document.getElementById("rRange");
const r_value = document.getElementById("r_value");
const mpLink = document.getElementById("mpChart");
const mainScript = document.getElementById("mainScript")
const slide_input = document.getElementById("slideRange");
const slide_value = document.getElementById("slide_value");

const dataset_id = mainScript.className.split(" ")[0]
let r, slide =3;
r_input.addEventListener("change", e=>{
    r_value.value = e.target.value;
    createR_chart(e.target.value,slide);
    r = e.target.value;
    mpLink.href = window.location.protocol + "//" + window.location.host + "/dataset/chart/" + dataset_id + `?r=${e.target.value}&period=${slide}`;

})

slide_input.addEventListener("change", e =>{
     slide_value.value = e.target.value;
    createR_chart(r, e.target.value);
    slide = e.target.value;
    mpLink.href = window.location.protocol + "//" + window.location.host + "/dataset/chart/" + dataset_id + `?r=${r}&period=${e.target.value}`;
})

async function toggle_chart(id) {
    const resp = await fetch(`/dataset/chart/data/${id}`);
    return await resp.json();
}

async function create_chart() {
   let ctx = document.getElementById("chart");
   const data = await toggle_chart(dataset_id);

   return new Chart(ctx,{
       type: 'line',
        data: {
          labels: data.labels,
          datasets: [{
            label: 'Values',
            data: data.values,
            borderWidth: 1
          }]
        },
        scales:{
           y:{
               title:{dispay:true,text: "Численность популяции (тыс. особей)"}
           },
            x:{
               tilte:{dispay:true,text: "Дата измерения"}
            }
        }
   })
}


function dPopulation(value, growth_rate, cary_capacity) {
    return growth_rate*value*(1-value/cary_capacity) ;
}

function simpleMovingAverage(arr, period) {
    let smaArray = [];
    for (let i = 0; i <= arr.length - period; i++) {
        let sum = 0;
        for (let j = 0; j < period; j++) {
            sum += arr[i + j];
        }
        smaArray.push(sum / period);
    }
    return smaArray;
}

function createR_chart(r, period){
    const first = chart.data.datasets[0].data[0];
    let data = [first]
    for (let i = 1; i < chart.data.labels.length; i++) {
        const v = dPopulation(data[i-1], r,125)
        data.push(v)
    }
    data = simpleMovingAverage(data, period).map(val=>val-first)
    let chart_data= [first]
    const part = (data[0]-first)/5;
    for (let i = 1; i < period; i++) {chart_data.push(chart_data[i-1]+part);}

    if (chart.data.datasets.length>1){
        chart.data.datasets.pop()
    }
    chart.data.datasets.push({
        label: "R chart",
        borderWidth: 1,
        data: chart_data.concat(data),
        borderColor: "#e07200",
        color:"#e07200",
        backgroundColor: "#e07200",
        borderDash: [2,2]
    })
    chart.update()
}

function add_duration(add_years) {
    const last_elems = chart.data.labels[chart.data.labels.length-1].split('/');
    const year = parseInt(last_elems[1])
    for (let i = 1; i < add_years+1; i++) {
       chart.data.labels.push(last_elems[0]+"/"+(year+i).toString());
    }
    chart.update()
    createR_chart(r,slide);

}

function load_matplotlib_chart(id) {
    "dataset/chart/"+id+ r_value.value?`?r=${r_value.value}`:""
}

create_chart().then(res => chart=res )
