import React from 'react'
import { NavLink } from 'react-router-dom'

const Register = () => {
  return (
    <div className='container mt-5'>
        <div className='row'>
            <div className='col-12 col-md-7 col-sm-6'>
                <h1>Welcome!</h1>
            </div>
            <div className='col-12 col-md-5 col-sm-6'>
                <form method='POST'>
                    <div className="form-group">
                        <label htmlFor="companyName">Company Name</label>
                        <input type="text" className="form-control" id="companyName" name="companyName"
                            placeholder="Enter your name" />                        
                    </div>

                    <div className="form-group">
                        <label htmlFor="email">Email</label>
                        <input type="email" className="form-control" id="email" name="email"
                            placeholder="Enter your Email" />                        
                    </div>

                    <div className="form-group">
                        <label htmlFor="phone">Phone No.</label>
                        <input type="tel" className="form-control" id="phone" name="phone"
                            placeholder="Enter your Phone No." />                        
                    </div>

                    <div className="form-group">
                        <label htmlFor="password">Password</label>
                        <input type="password" className="form-control" id="password" name="password"
                            placeholder="Enter your Password" />                        
                    </div>

                    <div className="form-group">
                        <label htmlFor="cpassword">Confirm password</label>
                        <input type="password" className="form-control" id="cpassword" name="cpassword"
                            placeholder="Confirm password" />                        
                    </div>

                    <NavLink to='/login'>Already Registered, then Login here!</NavLink><br /><br />
                    <button type="submit" className="btn btn-primary" id='register' name='register'>Register</button>
                    
                </form>
            </div>
        </div>
        
    </div>
  )
}

export default Register
