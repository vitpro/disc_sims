import React, { Component } from 'react';
import covenantData from '../data/covenant-data.json';
import SoulbindElement from "./SoulbindElement";
import LineTo, { SteppedLineTo, Line } from 'react-lineto';

export default class CovenantLoadout extends Component {

    constructor(props) {
        super(props);
        this.state = {
            currently_selected_covenant: 0,
            currently_selected_soulbind: [
                0, 0, 0, 0
            ],
            selected_covenant: [
                true, false, false, false
            ],
            selected_soulbind: [
                [true, false, false],
                [true, false, false],
                [true, false, false],
                [true, false, false]
            ],
        }
    }

    covenantClickHandler = (name, idx) => {
        const selected_covenant = this.state.selected_covenant.slice();
        selected_covenant[this.state.currently_selected_covenant] = false;
        selected_covenant[idx] = true;

        this.setState({
            ...this.state,
            selected_covenant: selected_covenant,
            currently_selected_covenant: idx,
        });

        // pass changes to App
        this.props.covenantChangeHandler({name:name, idx: idx});
    };

    soulbindClickHandler = (name, idx) => {
        const curr_soulbind_idx = this.state.currently_selected_soulbind[this.state.currently_selected_covenant];
        const soulbind_list = this.state.selected_soulbind.slice();
        const curr_selected_list = this.state.currently_selected_soulbind.slice();
        const _selected_soulbind = this.state.selected_soulbind[this.state.currently_selected_covenant].slice();
        _selected_soulbind[curr_soulbind_idx] = false;
        _selected_soulbind[idx] = true;

        soulbind_list[this.state.currently_selected_covenant] = _selected_soulbind;
        curr_selected_list[this.state.currently_selected_covenant] = idx;

        this.setState({
            ...this.state,
            currently_selected_soulbind: curr_selected_list,
            selected_soulbind: soulbind_list
        });

        //no need to pass anything to App
    };

    render() {
        const soulbinds = covenantData.covenants[this.state.currently_selected_covenant].soulbinds.slice();
        const backgroundImage = ({
           background: 'url(' + soulbinds[this.state.currently_selected_soulbind[
                                this.state.currently_selected_covenant
                                ]].background_img + ')'
        });

        return (
            <div className="conduitPickerContainer">
                <h1>Covenant picker here</h1>
                <div className="flexLeft conduitsContainer" style={backgroundImage}>
                    <div className="flexDown">
                        {soulbinds.map((elem, idx) => (
                            <SoulbindElement
                                index={idx}
                                key={elem.name + idx.toString()}
                                name={elem.name}
                                url={elem.img_url}
                                selected={this.state.selected_soulbind[this.state.currently_selected_covenant][idx]}
                                clickHandler={this.soulbindClickHandler}
                                noneSelected={false}
                            />
                        ))}
                    </div>
                    <div className="conduitTreeContainer">
                        <div className="block-A">
                            A
                        </div>
                        <div className="block-B">
                            B
                        </div>
                        <div className="block-C">
                            C
                        </div>

                        <Line y0={666} y1={666} x0={710} x1={784} borderColor="#fb1563" borderWidth={8} className="linexd"/>
                        <Line y0={710} y1={666} x0={776} x1={776} borderColor="#fb1563" borderWidth={8} className="linexd"/>

                        <Line y0={710} y1={666} x0={776} x1={776} borderColor="#fb1563" borderWidth={8} className="linexd"/>

                        <LineTo from="block-C" to="block-B" borderColor="#fb1563" borderWidth={8} className="linexd" />
                    </div>


                    <div className="conduitsRandomInfoBlock">
                        <div>
                            <h1 className="title">{soulbinds[this.state.currently_selected_soulbind[
                                this.state.currently_selected_covenant
                                ]].name}</h1>
                            <p className="infoParagraph">{soulbinds[this.state.currently_selected_soulbind[
                                this.state.currently_selected_covenant
                                ]].description}</p>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}