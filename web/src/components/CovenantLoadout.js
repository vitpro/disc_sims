import React, { Component } from 'react';
import covenantData from '../data/covenant-data.json';
import conduitTree from '../data/conduit-tree.json';
import SoulbindElement from "./SoulbindElement";
import LineTo, { SteppedLineTo, Line } from 'react-lineto';
import ConduitElement from "./ConduitElement";

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
            selected_conduits: [
                false, false, false, false, false, false, false, false, false, false, false, false, false, false, false
            ]
        };
        this.treeRef = React.createRef();
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

    conduitClickhandler = (name, idx, available) => {
        if (!available) return;
        const selected_conduits = this.state.selected_conduits.slice();
        selected_conduits[idx] = true;
        this.setState({
            ...this.state,
            selected_conduits: selected_conduits
        });
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

    calculateBlockPosition = (x, y) => {
        const offset = { x: 700, y: 700 };
        const x_coord = offset.x + x;
        const y_coord = offset.y + y;
        return {
            y: '' + y_coord + 'px',
            x: '' + x_coord + 'px'
        }
    };

    render() {
        const soulbinds = covenantData.covenants[this.state.currently_selected_covenant].soulbinds.slice();
        const backgroundImage = ({
           background: 'url(' +
           soulbinds[this.state.currently_selected_soulbind[this.state.currently_selected_covenant]].background_img
           + ')'
        });
        const conduits =
            soulbinds[this.state.currently_selected_soulbind[this.state.currently_selected_covenant]].conduits.slice();
        const tree_id =
            soulbinds[this.state.currently_selected_soulbind[this.state.currently_selected_covenant]].conduit_tree_id;
        const lines =
            conduitTree.tree_id[tree_id].lines.slice();

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
                    <div ref={this.treeRef}>

                        {conduits.map((conduit, idx) => {
                            // get the coordinates for this conduit component
                            const coords = conduitTree.tree_id[tree_id].conduits[idx];
                            return (
                                <ConduitElement
                                    index={idx}
                                    key={conduit.name + idx.toString()}
                                    url={conduit.img}
                                    selected={this.state.selected_conduits[idx]}
                                    available={true} // TODO implement available
                                    clickHandler={this.conduitClickhandler}
                                    coords_x={coords.x}
                                    coords_y={coords.y}
                                />
                            )
                        })}
                        {}
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