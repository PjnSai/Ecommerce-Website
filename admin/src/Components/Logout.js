import React, {useEffect, useState} from 'react'
import { NavLink, useNavigate } from 'react-router-dom'

const Logout = () => {

    const navigate = useNavigate();
    
    //console.log(token)

    const [show, setShow] = useState(false)


    const adminLogout = async() => {
        const token = localStorage.getItem('token')
    
        const res = await fetch('/logoutAdmin', {
            method:"POST",
            headers:{
                'Content-Type':'application/json'

            },
            body: JSON.stringify({

                "auth": token
            })
        });

        const data = await res.json();


        if(res.status === 201){

            setShow(true)
            await localStorage.removeItem('token',data.token)

            window.alert('Logout Successful')

            navigate('/login', {replace:true});
        }
        else{
            window.alert('Logout Failed')
            navigate('/')
        }

    }

    useEffect(() => {
        adminLogout()

}, [])

  return (
    <div>
        <h1>{show?'Logout Successfully' : 'Processing...'}</h1>
    </div>
  )
}

export default Logout
