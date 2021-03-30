window.onload = init;

function init(){
    abilityForm = document.querySelectorAll(".form-row")
    container = document.querySelector("#form-container")
    addButton = document.getElementById("add-form")
    removeButtons = document.getElementsByClassName("remove-form")
    totalForms = document.querySelector("#id_form-TOTAL_FORMS")
    formNum = abilityForm.length-1
    formID = abilityForm.length-1

    console.log('button: ',document.getElementById("add-form"))
    console.log(addButton)
    addButton.addEventListener('click', addForm)

    for (let i=0; i< removeButtons.length; i++) {
        removeButtons.item(i).addEventListener('click',removeForm)
    }
}



function addForm(e) {
    e.preventDefault()

    let newForm = abilityForm[0].cloneNode(true) //clones the ability form
    let formRegex = RegExp(`form-(\\d){1}-`,`g`)

    formNum++ //increment the form number
    formID++
    newForm.innerHTML = newForm.innerHTML.replace(formRegex, `form-${formNum}-`)
    newForm.id = 'form-' + formID + '-row'
    console.log(newForm.innerHTML)
    container.insertBefore(newForm,addButton) //inserts the new form at the end of the form
    let removeButtons = document.getElementsByClassName("remove-form")
    for (let i=0; i< removeButtons.length; i++) {
        removeButtons.item(i).addEventListener('click',removeForm)
    }

    totalForms.setAttribute('value',`${formNum+1}`)

}

function removeForm(e){
    e.preventDefault()
    console.log('test')
    console.log('removing row:' + this.id.replace('-rem','-row'))

    document.getElementById(this.id.replace('-rem','-row')).remove()
    formNum-- //decrement the form number
    totalForms.setAttribute('value',`${formNum+1}`)
    let i = 0
    abilityForms = document.querySelectorAll(".form-row")
}
