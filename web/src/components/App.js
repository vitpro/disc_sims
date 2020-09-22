import React, { Component } from "react";
import { render } from "react-dom";

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            data: {
                'spells': []
            },
            loaded: false,
            placeholder: "Loading"
        };
    }

    componentDidMount() {
        fetch("/get_spells")
            .then(resp => {
                if (resp.status > 400) {
                    return this.setState(() => {
                        return { placeholder: "Error loading spell data"};
                    });
                }
                return resp.json();
            })
            .then(data => {
                this.setState(() => {
                    return {
                        data,
                        loaded: true
                    };
                });
            });
    }

    render() {
        return (
            <div>
                <p>hi</p>
                <ul>

                    {this.state.data.spells.map(spell => {
                        return (
                            <li>{spell.name}</li>
                        );
                    })}

                </ul>
            </div>
        );
    }
}

export default App;

const container = document.getElementById("app");
render(<App />, container);