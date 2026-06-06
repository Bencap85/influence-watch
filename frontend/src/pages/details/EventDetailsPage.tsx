import { useNavigate } from 'react-router-dom';
import EventDetails from '../../components/EventDetails';


export default function EventDetailsPage({ }) {

    const navigate = useNavigate();

    return (
        <>
            <EventDetails />
        </>
    )
}