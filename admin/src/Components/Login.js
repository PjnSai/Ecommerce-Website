import React from 'react'
import { NavLink } from 'react-router-dom'

const Login = () => {
  return (
    <div className='container mt-5'>
        <div className='row'>


            <div className='col-sm-6 offset-md-3 offset-sm-1'>
                <form method='POST'>

                    <div className="form-group">
                        <label htmlFor="email">Email</label>
                        <input type="email" className="form-control" id="email" name="email"
                            placeholder="Enter your Email" />                        
                    </div>

                    <div className="form-group">
                        <label htmlFor="password">Password</label>
                        <input type="password" className="form-control" id="password" name="password"
                            placeholder="Enter your Password" />                        
                    </div>

                    <NavLink to='/register'>Didn't Registered, then register here!</NavLink><br /><br />
                    <button type="submit" className="btn btn-primary" id='login' name='login'>login</button>
                    
                </form>
            </div>
        </div>
        
    </div>
  )
}

export default Login
