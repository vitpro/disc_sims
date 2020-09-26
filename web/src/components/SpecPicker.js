import React, { Component } from 'react';
import specData from '../data/spec-data.json';
import SpecElement from "./SpecElement";

export default class SpecPicker extends Component {

    constructor(props) {
        super(props);
        this.state = {
            selected_spec: [
                false, false, false, false, false, false
            ],
            currently_selected: -1,
        }
    }

    specClickHandler = (name, idx) => {
        const selected_spec = this.state.selected_spec.slice();
        selected_spec[this.state.currently_selected] = false;
        selected_spec[idx] = true;

        this.setState({
            selected_spec: selected_spec,
            currently_selected: idx,
        });

        this.props.specChangeHandler({name: name, idx: idx});
    };

    render() {

        const noneSelected = this.state.currently_selected === -1;

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
                        noneSelected={noneSelected}
                    />
                ))}
            </div>
        );
    }
}