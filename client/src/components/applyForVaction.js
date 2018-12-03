import React, { Component } from 'react';
import axios from 'axios'


class ApplyForVaction extends Component {
    constructor(props){
        super(props)
        this.state ={
            startDate:'',
            endDate:'',
            userID:props.userID
        }
        this.submitForm = this.submitForm.bind(this)
    }

    onChange = ({ target: { name, value } }) => {
        this.setState({ [name]: value })
    }

    submitForm(e){
        e.preventDefault();
        console.log(this.state)
        const info ={
            startDate:this.state.startDate,
            endDate: this.state.endDate,
            userID:this.state.userID
        }
        axios.post('/api/requesttimeoff',{info})
            .then(res=>{
                console.log(res.data)
            })
    }

    render() {
        return (
            <div>
                <form onSubmit={this.submitForm}>
                <div className="form_element">
                Start Date
                <input 
                    data-date="" 
                    data-date-format="MM/DD/YYYY"
                    name='startDate'
                    placeholder="mm/dd/yyyy"
                    value={this.state.hireDate}
                    onChange={this.onChange}
                />
                </div>
                <div className="form_element">
                End Date
                <input 
                    data-date="" 
                    data-date-format="MM/DD/YYYY"
                    name='endDate'
                    placeholder="mm/dd/yyyy"
                    value={this.state.endDate}
                    onChange={this.onChange}
                />
                </div>
                <button type="submit" className="btn btn-info btn-sm">Submit</button>
                </form>
            </div>
        );
    }
}

export default ApplyForVaction;