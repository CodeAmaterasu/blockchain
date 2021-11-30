class Resources:

    def __init__(self) -> None:
        self.resources = []
        self.resources.append('Resource one')
        self.resources.append('Resource two')
        self.resources.append('Resource three')
        self.resources.append('Resource four')
        self.resources.append('Resource five')
        self.resources.append('Resource six')
        self.resources.append('Resource seven')
        self.resources.append('Resource eight')
        self.resources.append('Resource nine')

    def check_resource(self, resource: str):
        """
        Check if resource is available
        :param resource: Resource to check
        :return: if the resource is available
        """
        return resource in self.resources

    def get_resource(self, resource: str):
        for i in range(0, len(self.resources)):
            if self.resources[i] == resource:
                r = self.resources[i]
                self.resources.remove(r)
                return r
