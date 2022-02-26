//Variables
const dateEl = document.getElementById('id_date');
const selectEl = document.getElementById('id_meal');

//Date Picker Animations


M.Datepicker.init(dateEl, {
    format: 'yyyy-mm-dd',
    defaultDate: new Date(),
    setDefaultDate: true,
    autoClose: true

})

//select Widget Animations

M.FormSelect.init(selectEl);