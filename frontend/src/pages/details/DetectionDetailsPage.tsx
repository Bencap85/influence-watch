import { useNavigate } from 'react-router-dom';
import DetectionDetails from '../../components/DetectionDetails';


export default function DetectionDetailsPage({ }) {

    const navigate = useNavigate();

    return (
        <>
            <DetectionDetails />
        </>
    )
}