def get_client(af="coffea_casa"):
    if af == "coffea_casa":
        from dask.distributed import Client

        client = Client("tls://localhost:8786")

    elif af == "EAF":
        from htcdaskgateway import HTCGateway

        gateway = HTCGateway()
        cluster = gateway.new_cluster()
        cluster.scale(10)
        print("Please allow up to 60 seconds for HTCondor worker jobs to start")
        print(f"Cluster dashboard: https://dask-gateway.fnal.gov/clusters/{str(cluster.name)}/status")

        client = cluster.get_client()

    elif af == "cmsaf-dev":
        from dask_gateway import Gateway
        
        gateway = Gateway()
        clusters = gateway.list_clusters()
        # by default you will have at least one Dask gateway cluster, but here could be more
        # to shut down cluster please use: `cluster.shutdown()`
        cluster = gateway.connect(clusters[0].name)
        # adjust number of workers manually
        cluster.scale(50)
        
        client = cluster.get_client()

    elif af == "purdue-af":
        from dask_gateway import Gateway
        gateway = Gateway(
            "http://dask-gateway-k8s.geddes.rcac.purdue.edu/",
            proxy_address="traefik-dask-gateway-k8s.cms.geddes.rcac.purdue.edu:8786",
        )
        clusters = gateway.list_clusters()
        cluster = gateway.connect(clusters[0].name)
        cluster.scale(10)        
        client = cluster.get_client()

    elif af == "local":
        from dask.distributed import Client

        client = Client()

    elif af == "dirac":
        from dask_dirac import DiracCluster
        from dask.distributed import Client

        cluster = DiracCluster(
                        scheduler_options={"port": 8786},
                        dirac_sites="LCG.UKI-SOUTHGRID-RALPP.uk",
                        cert_path="/users/ak18773/SWIFT_HEP/dev_dirac/diracos/etc/grid-security/certificates",
                        owner_group="gridpp_user",
                        user_proxy="/tmp/x509up_u397871",
                        submission_url="https://diracdev.grid.hep.ph.ic.ac.uk:8444",
                        container="docker://sameriksen/dask:cms_agc",
                        nthreads=5,
                    )   

        cluster.scale(jobs=3)

        print("Workers can take a while to connect. Please be patient.")
        print(f"Cluster dashboard: {str(cluster.dashboard_link)}")

        client = Client(cluster)

    else:
        raise NotImplementedError(f"unknown analysis facility: {af}")

    return client

def get_triton_client(triton_url):
    
    import tritonclient.grpc as grpcclient
    triton_client = grpcclient.InferenceServerClient(url=triton_url, ssl=True)
    
    return triton_client
