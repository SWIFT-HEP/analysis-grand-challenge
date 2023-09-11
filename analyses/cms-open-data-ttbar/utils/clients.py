def get_client(af="coffea_casa"):
    if af == "coffea_casa":
        from dask.distributed import Client

        client = Client("tls://localhost:8786")

    elif af == "EAF":
        from lpcdaskgateway import LPCGateway

        gateway = LPCGateway()
        cluster = gateway.new_cluster()
        cluster.scale(10)
        print("Please allow up to 60 seconds for HTCondor worker jobs to start")
        print(f"Cluster dashboard: {str(cluster.dashboard_link)}")

        client = cluster.get_client()

    elif af == "local":
        from dask.distributed import Client

        client = Client()
        
    elif af == "DIRAC":
        from dask_dirac import DiracCluster
        from dask.distributed import Client
        
        cluster = DiracCluster(cores=8,
                       memory="24GB",
                       scheduler_options={"port": 8786},
                       dirac_site="LCG.UKI-SOUTHGRID-RALPP.uk",
                       cert_path="/users/ak18773/SWIFT_HEP/dev_dirac/diracos/etc/grid-security/certificates",
                       owner_group="gridpp_user",
                       user_proxy="/tmp/x509up_u397871",
                       submission_url="https://diracdev.grid.hep.ph.ic.ac.uk:8444",
                    )
        
        cluster.scale(jobs=5)
        
        print("Please allow up to 60 minutes for the first worker to connect.")
        print(f"Cluster dashboard: {str(cluster.dashboard_link)}")
        
        client = Client(cluster)

    else:
        raise NotImplementedError(f"unknown analysis facility: {af}")

    return client

def get_triton_client(triton_url):
    
    import tritonclient.grpc as grpcclient
    triton_client = grpcclient.InferenceServerClient(url=triton_url)
    
    return triton_client