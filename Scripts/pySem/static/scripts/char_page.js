let chart;

const r_input = document.getElementById("rRange");
const r_value = document.getElementById("r_value");
const mpLink = document.getElementById("mpChart");
const mainScript = document.getElementById("mainScript")

const dataset_id = mainScript.className.split(" ")[0]

r_input.addEventListener("change", e=>{
    r_value.value = e.target.value;
    createR_chart(e.target.value)
    mpLink.href = window.location.protocol + "//" + window.location.host + "/dataset/chart/" + dataset_id + `?r=${e.target.value}`;

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
        }
   })
}


function createR_chart(r){
    const max = Math.max(Math.max.apply(null,chart.data.datasets[0].data))
    const first = chart.data.datasets[0].data[0]/max;
    const data = [first]

    for (let i = 1; i < chart.data.labels.length; i++) {
        data.push(r*data[i-1]*(1-data[i-1]))
    }
    if (chart.data.datasets.length>1){
        chart.data.datasets.pop()
    }
    chart.data.datasets.push({
        label: "R chart",
        borderWidth: 1,
        data: data.map(val=>val*max),
        borderColor: "#e07200",
        color:"#e07200",
        backgroundColor: "#e07200",
        borderDash: [2,2]
    })
    chart.update()
}

function load_matplotlib_chart(id) {
    "dataset/chart/"+id+ r_value.value?`?r=${r_value.value}`:""
}

create_chart().then(res => chart=res )
