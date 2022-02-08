import React from "react";
import "./CompanyContact.css";
import { NotificationManager as nm } from "react-notifications";
import _ from "lodash";
import Loading from "../../box/Loading.jsx";
import Message from "../../box/Message.jsx";
import Contact from "../../button/Contact.jsx";
import { getRequest } from "../../../utils/request.jsx";

export default class CompanyContact extends React.Component {
	constructor(props) {
		super(props);

		this.refresh = this.refresh.bind(this);
		this.addAddress = this.addAddress.bind(this);

		this.state = {
			addresses: null,
			companyName: props.name,
			contactEnums: null,
		};
	}

	componentDidMount() {
		this.refresh();
	}

	refresh() {
		getRequest.call(this, "company/get_company_contacts/" + this.props.id, (data) => {
			this.setState({
				addresses: data,
			});
		}, (response) => {
			nm.warning(response.statusText);
		}, (error) => {
			nm.error(error.message);
		});

		getRequest.call(this, "contact/get_contact_enums", (data) => {
			this.setState({
				contactEnums: data,
			});
		}, (response) => {
			nm.warning(response.statusText);
		}, (error) => {
			nm.error(error.message);
		});
	}

	addAddress() {
		const addresses = _.cloneDeep(this.state.addresses);
		addresses.push({
			company_id: this.props.id,
			type: null,
			representative: null,
			name: null,
			value: null,
		});

		this.setState({ addresses });
	}

	changeState(field, value) {
		this.setState({ [field]: value });
	}

	render() {
		if (this.state.addresses === null) return <Loading height={300}/>;

		return (
			<div className={"row"}>
				<div className="col-md-12">
					<div className={"top-right-buttons"}>
						<button
							className={"blue-background"}
							onClick={() => this.addAddress()}>
							<i className="fas fa-plus"/> Add an empty contact point
						</button>
					</div>
					<h2>Contact points</h2>
				</div>
				<div className="col-md-12">
					{this.state.addresses.length > 0
						? this.state.addresses.map((a) => (
							<Contact
								key={a.id}
								info={a}
								enums={this.state.contactEnums}
								afterAction={this.refresh}
							/>
						))
						: <Message
							text={"No contact found on the database"}
							height={250}
						/>
					}
				</div>
			</div>
		);
	}
}
