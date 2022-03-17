import React from "react";
import Link from "next/link";
import { MDBCol, MDBContainer, MDBRow, MDBFooter } from 'mdbreact';


export default function TheFooter () {
  const logo = require("../../public/assets/AGVN_white_transparent.png");

  return (
    <MDBFooter color="blue darken-4" className="font-small pt-4 mt-4">
      <MDBContainer className="mt-5 mb-2 text-center text-md-left">
        <MDBRow>
          
          <MDBCol md="2" lg="2" xl="2" className="mb-3">
            <h5 className="text-uppercase font-weight-bold">
              <strong>Meta</strong>
            </h5>
            <hr className="blue-light accent-2 mb-4 mt-0 d-inline-block mx-auto" style={{ width: "60px" }}/>
              <p><Link href="/about">About</Link></p>
              <p>Contact us</p>
              <p>Need help?</p>
              <p>Translator</p>
          </MDBCol>
          <MDBCol md="3" lg="2" xl="2" className="mb-3">
            <h5 className="text-uppercase font-weight-bold">
              <strong>Terms</strong>
            </h5>
            <hr className="blue-light accent-2 mb-4 mt-0 d-inline-block mx-auto" style={{ width: "60px" }}/>
              <p>Privacy</p>
              <p>Terms of use</p>
              <p>SMS</p>
              <p>Complaints</p>
          </MDBCol>
          <MDBCol md="4" lg="3" xl="3" className="mb-3">
            <h5 className="text-uppercase font-weight-bold">
              <strong>Usage</strong>
            </h5>
            <hr className="blue-light accent-2 mb-4 mt-0 d-inline-block mx-auto" style={{ width: "60px" }}/>
              <p>Email: agvn@agvn.info</p>
              <p>Report fraud</p>
              <p>Social media</p>
              <p>News articles</p>
          </MDBCol>
            <MDBCol md="4" lg="5" xl="4" className="mb-3 text-md-center">
            <h5>
              <img
                src={logo}
                width='274.96'
                height='560'
                alt="AGVN Logo"
                style={{cursor:'pointer', marginLeft:'auto', marginRight:'auto'}}
              />
            </h5>
            <h5 className="text-uppercase mb-4 font-weight-bold">
              The future has never been so great
            </h5>
            </MDBCol>
        </MDBRow>
      </MDBContainer>
      <div className="footer-copyright text-center py-3">
        <MDBContainer fluid>
          &copy; {new Date().getFullYear()} Copyright: <a href="https://www.mdbootstrap.com"> AGVN System </a>
        </MDBContainer>
      </div>
    </MDBFooter>
  )
}
