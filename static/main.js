const userForm = document.querySelector('#userForm');

let users = []
let editing = false
let userId = null

window.addEventListener('DOMContentLoaded', async () => {
    const response = await fetch('/api/users');
    const data = await response.json()
    users = data
    renderUser(users)
});

userForm.addEventListener('submit', async e => {

    e.preventDefault()

    const procesador = userForm['procesador'].value
    const costo = userForm['costo'].value
    const marca = userForm['marca'].value
    const numero = userForm['numero'].value

    if (!editing){
        const response = await fetch('/api/users', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                procesador,
                costo,
                marca,
                numero,
            }),
        });
    
        const data = await response.json();

        users.unshift(data);
        console.log("hola mundo")
    } else{
        const response = await fetch(`/api/users/${userId}`, {
            method: "PUT",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                procesador,
                costo,
                marca,
                numero,
            }),
        })
        const updateUser = await response.json()
        users = users.map(user => user.id === updateUser.id ? updateUser : user)
        renderUser(users)
    }

    renderUser(users);

    userForm.reset();


});

function renderUser(users) {
    const userList = document.querySelector('#userList')
    userList.innerHTML = ''

    users.forEach(user => {
        const userItem = document.createElement('li')
        userItem.classList = 'list-group-item list-group-item-dark my-2'
        userItem.innerHTML = `
       <header class="d-flex justify-content-between aling-items-center">
          <h5>${user.procesador}</h5>
          <div>
            <button class=" btn-delete btn btn-primary btn-sm">Eliminar</button>
            <button class=" btn-edit btn btn-dark btn-sm">Editar</button>
          </div>        
       </header>
       <p>${user.costo}</p>
       <p>${user.marca}</p>
       <p>${user.numero}</p>
       
    `
        const btnDelete = userItem.querySelector('.btn-delete');
        btnDelete.addEventListener('click', async () => {
            const response = await fetch(`/api/users/${user.id}`, {
                method: 'DELETE'
            })
            const data = await response.json();

            users = users.filter(user => user.id !== data.id);
            renderUser(users);

        })
        
        const btnEdit = userItem.querySelector('.btn-edit');

        btnEdit.addEventListener('click', async e => {

            const response = await fetch(`/api/users/${user.id}`);
            const data = await response.json();

            userForm["procesador"].value = data.procesador;
            userForm["costo"].value = data.costo;
            userForm["marca"].value = data.marca;
            userForm["numero"].value = data.numero;

            editing = true
            userId = data.id
        })

        userList.append(userItem);


    })
}
