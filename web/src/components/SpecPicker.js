import React, { Component } from 'react';
import specData from '../data/spec-data.json';
import SpecElement from "./SpecElement";

export default class SpecPicker extends Component {

    constructor(props) {
        super(props);
        this.state = {
            selected_spec: [
                true, false, false, false, false, false
            ],
            currently_selected: 0
        }
    }

    specClickHandler = idx => {
        const selected_spec = this.state.selected_spec.slice();
        selected_spec[this.state.currently_selected] = false;
        selected_spec[idx] = true;

        this.setState({
            selected_spec: selected_spec,
            currently_selected: idx,
        })

        // TODO send back to App
    };

    render() {
        return (
            <div className="specPickerGrid">
                {specData["specs"].map((spec, idx) => (
                    <SpecElement
                        index={idx}
                        key={spec.name + idx.toString()}
                        name={spec.name}
                        url={spec.url}
                        selected={this.state.selected_spec[idx]}
                        clickHandler={this.specClickHandler}
                    />
                ))}
            </div>
        );
    }
}