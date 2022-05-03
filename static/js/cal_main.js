// import {mockData} from './mockData.js';
import {Calendar} from './calendar.js';

document.addEventListener("DOMContentLoaded", async ()=>{
    const cal = Calendar('calendar');
    cal.bindData(mockData);
    cal.render();
});